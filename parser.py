import ply.yacc as yacc
from lexer import tokens

# ==========================================
# 1. DEFINICJE WĘZŁÓW AST (Drzewa Składniowego)
# ==========================================

class ProgramNode:
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self): return f"Program(\n  " + "\n  ".join(map(str, self.statements)) + "\n)"

class AssignNode:
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self): return f"Assign({self.name} = {self.value})"

class PrintNode:
    def __init__(self, expr_list):
        self.expr_list = expr_list
    def __repr__(self): return f"Print({self.expr_list})"

class IfNode:
    def __init__(self, condition, true_branch, false_branch=None):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch
    def __repr__(self): 
        res = f"If({self.condition}) {{\n    {self.true_branch}\n  }}"
        if self.false_branch: res += f" Else {{\n    {self.false_branch}\n  }}"
        return res

class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    def __repr__(self): return f"While({self.condition}) {{\n    {self.body}\n  }}"

class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __repr__(self): return f"({self.left} {self.op} {self.right})"

class UnaryOpNode:
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
    def __repr__(self): return f"({self.op} {self.expr})"

class LiteralNode:
    def __init__(self, value, v_type):
        self.value = value
        self.v_type = v_type # 'int', 'float', 'string', 'bool'
    def __repr__(self): 
        if self.v_type == 'string': return f'"{self.value}"'
        return str(self.value)

class VarNode:
    def __init__(self, name):
        self.name = name
    def __repr__(self): return f"Var({self.name})"

class ListAppendNode:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
    def __repr__(self): return f"ListAppend({self.name} <- {self.expr})"

class ListLiteralNode:
    def __init__(self, elements):
        self.elements = elements
    def __repr__(self): return f"List[{self.elements}]"

class ListAccessNode:
    def __init__(self, name, index_expr):
        self.name = name
        self.index_expr = index_expr
    def __repr__(self): return f"ListAccess({self.name}[{self.index_expr}])"

class ListLenNode:
    def __init__(self, name):
        self.name = name
    def __repr__(self): return f"ListLen({self.name})"

class CastNode:
    def __init__(self, cast_type, expr):
        self.cast_type = cast_type
        self.expr = expr
    def __repr__(self): return f"Cast<{self.cast_type}>({self.expr})"

class InputNode:
    def __init__(self, prompt_expr=None):
        self.prompt_expr = prompt_expr
    def __repr__(self): 
        if self.prompt_expr: return f"Input({self.prompt_expr})"
        return "Input()"

class ExitNode:
    def __repr__(self): return "Exit()"


# ==========================================
# 2. REGUŁY GRAMATYCZNE PARSERA (YACC)
# ==========================================

# --- Sekcja: Struktura programu ---
def p_program(p):
    '''program : statements'''
    p[0] = ProgramNode(p[1])

def p_statements_multiple(p):
    '''statements : statements statement'''
    # Ignorujemy puste instrukcje (np. same znaki nowej linii)
    if p[2] is not None:
        p[1].append(p[2])
    p[0] = p[1]

def p_statements_single(p):
    '''statements : statement'''
    p[0] = [p[1]] if p[1] is not None else []

def p_statement(p):
    '''statement : assignment NEWLINE
                 | print_stmt NEWLINE
                 | if_stmt
                 | while_stmt
                 | list_append NEWLINE
                 | exit_stmt NEWLINE'''
    p[0] = p[1]

def p_statement_empty(p):
    '''statement : NEWLINE'''
    p[0] = None

def p_assignment(p):
    '''assignment : ID ASSIGN expression'''
    p[0] = AssignNode(p[1], p[3])

def p_list_append(p):
    '''list_append : ID APPEND expression'''
    p[0] = ListAppendNode(p[1], p[3])

def p_print_stmt(p):
    '''print_stmt : PRINT expression_list'''
    p[0] = PrintNode(p[2])

def p_expression_list_multiple(p):
    '''expression_list : expression_list COMMA expression'''
    p[1].append(p[3])
    p[0] = p[1]

def p_expression_list_single(p):
    '''expression_list : expression'''
    p[0] = [p[1]]

# --- Sekcja: Przepływ sterowania ---
def p_if_stmt(p):
    '''if_stmt : IF expression LBRACE statements RBRACE'''
    p[0] = IfNode(p[2], p[4])

def p_if_else_stmt(p):
    '''if_stmt : IF expression LBRACE statements RBRACE ELSE LBRACE statements RBRACE'''
    p[0] = IfNode(p[2], p[4], p[8])

def p_while_stmt(p):
    '''while_stmt : WHILE expression LBRACE statements RBRACE'''
    p[0] = WhileNode(p[2], p[4])

def p_exit_stmt(p):
    '''exit_stmt : EXIT'''
    p[0] = ExitNode()

# --- Sekcja: Wyrażenia i Hierarchia Operatorów ---
def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term
                  | expression OR term'''
    p[0] = BinOpNode(p[1], p[2], p[3])

def p_expression_term(p):
    '''expression : term'''
    p[0] = p[1]

def p_term_binop(p):
    '''term : term MULTIPLY factor
            | term DIVIDE factor
            | term AND factor'''
    p[0] = BinOpNode(p[1], p[2], p[3])

def p_term_factor(p):
    '''term : factor'''
    p[0] = p[1]

def p_factor_comparison(p):
    '''factor : factor EQ comparison
              | factor NEQ comparison
              | factor LT comparison
              | factor GT comparison
              | factor LE comparison
              | factor GE comparison'''
    p[0] = BinOpNode(p[1], p[2], p[3])

def p_factor_comp(p):
    '''factor : comparison'''
    p[0] = p[1]

# --- Sekcja: Operandy i funkcje wbudowane ---
def p_comparison_parens(p):
    '''comparison : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_comparison_not(p):
    '''comparison : NOT comparison'''
    p[0] = UnaryOpNode(p[1], p[2])

def p_comparison_literal_number(p):
    '''comparison : NUMBER'''
    v_type = 'float' if isinstance(p[1], float) else 'int'
    p[0] = LiteralNode(p[1], v_type)

def p_comparison_literal_string(p):
    '''comparison : STRING'''
    p[0] = LiteralNode(p[1], 'string')

def p_comparison_literal_bool(p):
    '''comparison : TRUE
                  | FALSE'''
    # ✅ to True, ❌ to False
    val = True if p[1] == '✅' else False
    p[0] = LiteralNode(val, 'bool')

def p_comparison_var(p):
    '''comparison : ID'''
    p[0] = VarNode(p[1])

def p_comparison_others(p):
    '''comparison : list_literal
                  | list_access
                  | list_len
                  | casting_op
                  | input_op'''
    p[0] = p[1]

def p_list_literal(p):
    '''list_literal : LBRACKET expression_list RBRACKET'''
    p[0] = ListLiteralNode(p[2])

def p_list_literal_empty(p):
    '''list_literal : LBRACKET RBRACKET'''
    p[0] = ListLiteralNode([])

def p_list_access(p):
    '''list_access : ID AT expression'''
    p[0] = ListAccessNode(p[1], p[3])

def p_list_len(p):
    '''list_len : LEN ID'''
    p[0] = ListLenNode(p[2])

def p_casting_op(p):
    '''casting_op : INT_CAST LPAREN expression RPAREN
                  | FLOAT_CAST LPAREN expression RPAREN
                  | STR_CAST LPAREN expression RPAREN'''
    cast_map = {'🔢': 'int', '📉': 'float', '🔤': 'str'}
    p[0] = CastNode(cast_map[p[1]], p[3])

def p_input_op_with_prompt(p):
    '''input_op : INPUT LPAREN expression RPAREN'''
    p[0] = InputNode(p[3])

def p_input_op_empty(p):
    '''input_op : INPUT LPAREN RPAREN'''
    p[0] = InputNode()

# --- Sekcja: Obsługa błędów ---
def p_error(p):
    if p:
        print(f"[Błąd składniowy] Nieoczekiwany token '{p.value}' (typ: {p.type}) w linii {p.lineno}")
    else:
        print("[Błąd składniowy] Nieoczekiwany koniec pliku (EOF)")

# ==========================================
# 3. INICJALIZACJA PARSERA
# ==========================================
parser = yacc.yacc()

# --- BLOK TESTOWY ---
if __name__ == "__main__":
    # Testowy kod w EmoLang
    kod_testowy = """
    # Inicjalizacja
    liczba 📦 10 🔚
    
    # Warunek logiczny
    ❓ liczba 👉 5 🧱
        📢 💬 Jest wieksze! 💬 🔚
    🛑 💡 🧱
        📢 💬 Jest mniejsze! 💬 🔚
    🛑
    """
    
    print("Budowanie Drzewa Składniowego (AST)...\n")
    # Wywołanie parsera na kodzie testowym
    ast = parser.parse(kod_testowy)
    
    if ast:
        print("Udało się! Oto wygenerowane drzewo AST:\n")
        print(ast)
