# parser_yacc.py
import ply.yacc as yacc
from lexer import tokens
from ast_nodes import *

# Priorytety operatorów (od najniższego do najwyższego)
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ', 'LT', 'GT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('right', 'NOT'),
)

def p_program(p):
    '''program : statements'''
    p[0] = BlockNode(p[1])

def p_statements_multiple(p):
    '''statements : statements statement'''
    p[0] = p[1] + [p[2]]

def p_statements_single(p):
    '''statements : statement'''
    p[0] = [p[1]]

def p_statement(p):
    '''statement : assignment NEWLINE
                 | print_stmt NEWLINE
                 | if_stmt
                 | NEWLINE'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : ID ASSIGN expression'''
    p[0] = AssignNode(p[1], p[3])

def p_print_stmt(p):
    '''print_stmt : PRINT expression'''
    p[0] = PrintNode(p[2])

def p_if_stmt(p):
    '''if_stmt : IF expression LBRACE statements RBRACE'''
    p[0] = IfNode(p[2], BlockNode(p[4]))

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULT expression
                  | expression DIV expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression LT expression
                  | expression GT expression'''
    p[0] = BinOpNode(p[1], p[2], p[3])

def p_expression_val(p):
    '''expression : NUMBER
                  | STRING
                  | TRUE
                  | FALSE
                  | ID'''
    if isinstance(p[1], (int, float)): p[0] = NumberNode(p[1])
    elif p[1] == '✅': p[0] = BooleanNode(True)
    elif p[1] == '❌': p[0] = BooleanNode(False)
    elif isinstance(p[1], str) and not p[1].isidentifier(): p[0] = StringNode(p[1]) # proste rozróżnienie
    else: p[0] = VarNode(p[1])

def p_error(p):
    if p:
        print(f"🔥 Błąd składniowy przy tokenie '{p.value}' w linii {p.lineno}")
    else:
        print("🔥 Błąd składniowy: Niespodziewany koniec pliku")

parser = yacc.yacc()
