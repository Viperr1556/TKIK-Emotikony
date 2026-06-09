# -*- coding: utf-8 -*-
"""
EmoLang - analizator składniowy (parser).

Zadanie parsera: ze strumienia tokenów (od skanera) zbudować DRZEWO
SKŁADNIOWE (AST) zgodne z gramatyką języka. Każda reguła gramatyki ma
"akcję" - kawałek Pythona, który tworzy odpowiedni węzeł z ast_nodes.

Używamy generatora parserów PLY (Python Lex-Yacc), moduł `ply.yacc`.
Generuje on parser typu LALR(1).

STRUKTURA GRAMATYKI:
- jednorodny poziom instrukcji: jeden `statement`, jeden wspólny `block`
  (używany tak samo przez if/while/funkcje);
- WARSTWOWY poziom wyrażeń: każdy priorytet operatora to osobny nieterminał
  (or_expr -> and_expr -> not_expr -> comparison -> additive ->
   multiplicative -> unary -> postfix -> primary). Dzięki temu priorytety i
  łączność wynikają WPROST ZE STRUKTURY GRAMATYKI - nie potrzeba tabeli
  `precedence`, a gramatyka jest wolna od konfliktów shift/reduce.
"""

import ply.yacc as yacc
from lexer import tokens, find_column          # tokens są wymagane przez PLY
from ast_nodes import *


# ===== Korzeń: program to ciąg instrukcji ==================================

def p_program(p):
    'program : statements'
    p[0] = BlockNode(p[1])

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]


# ===== Instrukcje ==========================================================
# "Proste" instrukcje kończą się znacznikiem 🔚 (END).
# "Złożone" (if/while/funkcja) kończą się własnym blokiem 🛑 - bez 🔚.

def p_statement(p):
    '''statement : assignment END
                 | print_stmt END
                 | append_stmt END
                 | return_stmt END
                 | expression END
                 | EXIT END
                 | if_stmt
                 | while_stmt
                 | func_def'''
    if len(p) == 3:
        # 🏁 (EXIT) nie tworzy węzła - to tylko sygnał "koniec programu".
        p[0] = None if p.slice[1].type == 'EXIT' else p[1]
    else:
        p[0] = p[1]

def p_block(p):
    '''block : LBRACE statements RBRACE
             | LBRACE RBRACE'''
    p[0] = BlockNode(p[2]) if len(p) == 4 else BlockNode([])


# ===== Przypisanie, wypisywanie, listy =====================================

def p_assignment(p):
    'assignment : ID ASSIGN expression'
    p[0] = AssignNode(p[1], p[3])

def p_print_stmt(p):
    'print_stmt : PRINT arglist'
    p[0] = PrintNode(p[2])

def p_append_stmt(p):
    'append_stmt : ID APPEND expression'
    p[0] = AppendNode(p[1], p[3])


# ===== Sterowanie ==========================================================

def p_if_stmt(p):
    '''if_stmt : IF expression block
               | IF expression block ELSE block'''
    else_block = p[5] if len(p) == 6 else None
    p[0] = IfNode(p[2], p[3], else_block)

def p_while_stmt(p):
    'while_stmt : WHILE expression block'
    p[0] = WhileNode(p[2], p[3])


# ===== Funkcje (oraz return - kontrola semantyczna) ========================

def p_func_def(p):
    '''func_def : FUNC ID LPAREN params RPAREN block
                | FUNC ID LPAREN RPAREN block'''
    if len(p) == 7:
        p[0] = FuncDefNode(p[2], p[4], p[6])
    else:
        p[0] = FuncDefNode(p[2], [], p[5])

def p_params(p):
    '''params : params COMMA ID
              | ID'''
    p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]

def p_return_stmt(p):
    'return_stmt : RETURN expression'
    p[0] = ReturnNode(p[2])


# ===== Wyrażenia: gramatyka WARSTWOWA ======================================
# Każdy poziom odwołuje się tylko do poziomu wiążącego mocniej. Lewa rekurencja
# = łączność lewostronna (a-b-c = (a-b)-c). Operatory przedrostkowe (🚫, 📏,
# unarny ➖) i indeksowanie (🎯) mają własne poziomy. Brak tabeli precedence.

def p_expression(p):
    'expression : or_expr'
    p[0] = p[1]

def p_or_expr(p):
    '''or_expr : or_expr OR and_expr
               | and_expr'''
    p[0] = BinOpNode(p[1], 'OR', p[3]) if len(p) == 4 else p[1]

def p_and_expr(p):
    '''and_expr : and_expr AND not_expr
                | not_expr'''
    p[0] = BinOpNode(p[1], 'AND', p[3]) if len(p) == 4 else p[1]

def p_not_expr(p):
    '''not_expr : NOT not_expr
                | comparison'''
    p[0] = UnaryOpNode('NOT', p[2]) if len(p) == 3 else p[1]

def p_comparison(p):
    '''comparison : comparison EQ  additive
                  | comparison NEQ additive
                  | comparison LT  additive
                  | comparison GT  additive
                  | comparison LE  additive
                  | comparison GE  additive
                  | additive'''
    p[0] = BinOpNode(p[1], p.slice[2].type, p[3]) if len(p) == 4 else p[1]

def p_additive(p):
    '''additive : additive PLUS  multiplicative
                | additive MINUS multiplicative
                | multiplicative'''
    p[0] = BinOpNode(p[1], p.slice[2].type, p[3]) if len(p) == 4 else p[1]

def p_multiplicative(p):
    '''multiplicative : multiplicative TIMES  unary
                      | multiplicative DIVIDE unary
                      | unary'''
    p[0] = BinOpNode(p[1], p.slice[2].type, p[3]) if len(p) == 4 else p[1]

def p_unary(p):
    '''unary : MINUS unary
             | LEN unary
             | postfix'''
    if len(p) == 3:
        p[0] = UnaryOpNode('NEG', p[2]) if p.slice[1].type == 'MINUS' else LenNode(p[2])
    else:
        p[0] = p[1]

def p_postfix(p):
    '''postfix : postfix AT primary
               | primary'''
    p[0] = IndexNode(p[1], p[3]) if len(p) == 4 else p[1]


# ----- primary: wartości podstawowe i konstrukcje "domknięte" --------------

def p_primary_cast(p):
    'primary : NUM_CAST LPAREN expression RPAREN'
    p[0] = CastNode(p[3])

def p_primary_list(p):
    '''primary : LBRACKET arglist RBRACKET
               | LBRACKET RBRACKET'''
    p[0] = ListNode(p[2]) if len(p) == 4 else ListNode([])

def p_primary_call(p):
    '''primary : CALL ID LPAREN arglist RPAREN
               | CALL ID LPAREN RPAREN'''
    p[0] = CallNode(p[2], p[4] if len(p) == 6 else [])

def p_primary_input(p):
    'primary : INPUT'
    p[0] = InputNode()

def p_primary_group(p):
    'primary : LPAREN expression RPAREN'
    p[0] = p[2]

def p_primary_number(p):
    'primary : NUMBER'
    p[0] = NumberNode(p[1])

def p_primary_string(p):
    'primary : STRING'
    p[0] = StringNode(p[1])

def p_primary_true(p):
    'primary : TRUE'
    p[0] = BoolNode(True)

def p_primary_false(p):
    'primary : FALSE'
    p[0] = BoolNode(False)

def p_primary_var(p):
    'primary : ID'
    p[0] = VarNode(p[1])


# ===== Listy argumentów / elementów ========================================

def p_arglist(p):
    '''arglist : arglist COMMA expression
               | expression'''
    p[0] = p[1] + [p[3]] if len(p) == 4 else [p[1]]


# ===== Błąd składniowy =====================================================

def p_error(p):
    if p:
        column = find_column(p.lexer.lexdata, p)
        print(f"🔥 Błąd składniowy: nieoczekiwany token '{p.value}' "
              f"(linia {p.lineno}, kolumna {column})")
    else:
        print("🔥 Błąd składniowy: nieoczekiwany koniec programu")


# Budujemy gotowy parser.
parser = yacc.yacc()
