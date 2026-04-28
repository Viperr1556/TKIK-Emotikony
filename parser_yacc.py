import ply.yacc as yacc
from lexer import tokens
from ast_nodes import *

precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('right', 'NOT'),
)

def p_program(p):
    '''program : statements'''
    p[0] = BlockNode(p[1])

def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 3: p[0] = p[1] + [p[2]]
    else: p[0] = [p[1]]

def p_statement(p):
    '''statement : assignment NEWLINE
                 | print_stmt NEWLINE
                 | function_def
                 | return_stmt NEWLINE
                 | expression NEWLINE
                 | if_stmt
                 | NEWLINE'''
    p[0] = p[1]

# Definicja funkcji
def p_function_def(p):
    '''function_def : FUNC_DEF ID INPUT params LBRACE statements RBRACE
                    | FUNC_DEF ID INPUT LBRACE statements RBRACE'''
    if len(p) == 8: p[0] = FuncDefNode(p[2], p[4], BlockNode(p[6]))
    else: p[0] = FuncDefNode(p[2], [], BlockNode(p[5]))

def p_params(p):
    '''params : params COMMA ID
              | ID'''
    if len(p) == 4: p[0] = p[1] + [p[3]]
    else: p[0] = [p[1]]

def p_return_stmt(p):
    '''return_stmt : RETURN expression'''
    p[0] = ReturnNode(p[2])

def p_assignment(p):
    '''assignment : ID ASSIGN expression'''
    p[0] = AssignNode(p[1], p[3])

def p_print_stmt(p):
    '''print_stmt : PRINT expression_list'''
    p[0] = PrintNode(p[2])

def p_expression_list(p):
    '''expression_list : expression_list COMMA expression
                       | expression'''
    if len(p) == 4: p[0] = p[1] + [p[3]]
    else: p[0] = [p[1]]

def p_if_stmt(p):
    '''if_stmt : IF expression LBRACE statements RBRACE
               | IF expression LBRACE statements RBRACE ELSE LBRACE statements RBRACE'''
    t_block = BlockNode(p[4])
    f_block = BlockNode(p[8]) if len(p) > 6 else None
    p[0] = IfNode(p[2], t_block, f_block)

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULTIPLY expression
                  | expression DIVIDE expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression LT expression
                  | expression GT expression'''
    p[0] = BinOpNode(p[1], p[2], p[3])

def p_expression_call(p):
    '''expression : CALL ID INPUT args RBRACE
                  | CALL ID INPUT RBRACE'''
    if len(p) == 6: p[0] = CallNode(p[2], p[4])
    else: p[0] = CallNode(p[2], [])

def p_args(p):
    '''args : args COMMA expression
            | expression'''
    if len(p) == 4: p[0] = p[1] + [p[3]]
    else: p[0] = [p[1]]

def p_expression_atom(p):
    '''expression : NUMBER
                  | STRING
                  | TRUE
                  | FALSE
                  | ID'''
    if isinstance(p[1], (int, float)): p[0] = NumberNode(p[1])
    elif p[1] == '✅': p[0] = NumberNode(True)
    elif p[1] == '❌': p[0] = NumberNode(False)
    elif isinstance(p[1], str) and p[1].isidentifier(): p[0] = VarNode(p[1])
    else: p[0] = StringNode(p[1])

def p_error(p):
    if p: print(f"Błąd składniowy przy tokenie '{p.value}' w linii {p.lineno}")
    else: print("Błąd składniowy na końcu pliku")

parser = yacc.yacc()
