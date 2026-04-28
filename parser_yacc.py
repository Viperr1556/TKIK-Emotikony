import ply.yacc as yacc
from lexer import tokens
from ast_nodes import *

# Pełna tabela priorytetów (rozwiązuje 24 konflikty shift/reduce)
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('left', 'AT'),
    ('right', 'NOT', 'LEN'),
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
                 | while_stmt
                 | append_stmt NEWLINE
                 | EXIT NEWLINE
                 | NEWLINE'''
    if len(p) == 2:
        if p[1] == '🔚': p[0] = None
        else: p[0] = p[1]
    else:
        if p[1] == '🏁': p[0] = None
        else: p[0] = p[1]

def p_function_def(p):
    '''function_def : FUNC_DEF ID INPUT LPAREN params RPAREN LBRACE statements RBRACE
                    | FUNC_DEF ID INPUT LPAREN RPAREN LBRACE statements RBRACE'''
    if len(p) == 10: p[0] = FuncDefNode(p[2], p[5], BlockNode(p[8]))
    else: p[0] = FuncDefNode(p[2], [], BlockNode(p[7]))

def p_params(p):
    '''params : params COMMA ID
              | ID'''
    if len(p) == 4: p[0] = p[1] + [p[3]]
    else: p[0] = [p[1]]
        
def p_expression_unary_minus(p):
    '''expression : MINUS expression %prec NOT'''
    p[0] = BinOpNode(NumberNode(0), '➖', p[2])
    
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

def p_while_stmt(p):
    '''while_stmt : WHILE expression LBRACE statements RBRACE'''
    p[0] = WhileNode(p[2], BlockNode(p[4]))

def p_append_stmt(p):
    '''append_stmt : ID APPEND expression'''
    p[0] = ListOpNode('APPEND', p[1], p[3])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MULTIPLY expression
                  | expression DIVIDE expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression LT expression
                  | expression GT expression
                  | expression LE expression
                  | expression GE expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = BinOpNode(p[1], p[2], p[3])

def p_expression_unary(p):
    '''expression : NOT expression'''
    p[0] = BinOpNode(None, 'NOT', p[2])

def p_expression_cast(p):
    '''expression : INT_CAST LPAREN expression RPAREN
                  | FLOAT_CAST LPAREN expression RPAREN
                  | STR_CAST LPAREN expression RPAREN'''
    if p[1] == '🔢': p[0] = CastNode('INT', p[3])
    elif p[1] == '📉': p[0] = CastNode('FLOAT', p[3])
    elif p[1] == '🔤': p[0] = CastNode('STR', p[3])

def p_expression_list_literal(p):
    '''expression : LBRACKET expression_list RBRACKET
                  | LBRACKET RBRACKET'''
    if len(p) == 4: p[0] = ListNode(p[2])
    else: p[0] = ListNode([])

def p_expression_list_op(p):
    '''expression : expression AT expression
                  | LEN expression'''
    if p[1] == '📏': p[0] = ListOpNode('LEN', p[2])
    else: p[0] = ListOpNode('AT', p[1], p[3])

def p_expression_call(p):
    '''expression : CALL ID INPUT LPAREN args RPAREN
                  | CALL ID INPUT LPAREN RPAREN'''
    if len(p) == 7: p[0] = CallNode(p[2], p[5])
    else: p[0] = CallNode(p[2], [])

def p_expression_input(p):
    '''expression : INPUT LPAREN RPAREN'''
    p[0] = InputNode()

def p_expression_group(p):
    '''expression : LPAREN expression RPAREN'''
    p[0] = p[2]

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
    if p: print(f"🔥 Błąd składniowy przy tokenie '{p.value}' w linii {p.lineno}")
    else: print("🔥 Błąd składniowy na końcu pliku")

parser = yacc.yacc()
