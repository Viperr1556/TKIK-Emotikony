import ply.lex as lex

tokens = (
    'ID', 'NUMBER', 'STRING',
    'ASSIGN', 'TRUE', 'FALSE',
    'INT_CAST', 'FLOAT_CAST', 'STR_CAST',
    'LBRACKET', 'RBRACKET', 'AT', 'LEN', 'APPEND',
    'PRINT', 'INPUT', 'COMMA',
    'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE',
    'OR', 'AND', 'NOT',
    'EQ', 'NEQ', 'LE', 'GE', 'LT', 'GT',
    'IF', 'ELSE', 'WHILE',
    'LBRACE', 'RBRACE', 'NEWLINE', 'EXIT',
    'LPAREN', 'RPAREN',
    'FUNC_DEF', 'CALL', 'RETURN'
)

t_FUNC_DEF   = r'🎁'
t_CALL       = r'🎈'
t_RETURN     = r'↪️'
t_ASSIGN     = r'📦'
t_TRUE       = r'✅'
t_FALSE      = r'❌'
t_INT_CAST   = r'🔢'
t_FLOAT_CAST = r'📉'
t_STR_CAST   = r'🔤'
t_LBRACKET   = r'📂'
t_RBRACKET   = r'📁'
t_AT         = r'🎯'
t_LEN        = r'📏'
t_APPEND     = r'🖇️'
t_PRINT      = r'📢'
t_INPUT      = r'📥'
t_COMMA      = r'📍'
t_PLUS       = r'➕'
t_MINUS      = r'➖'
t_MULTIPLY   = r'✖️'
t_DIVIDE     = r'➗'
t_OR         = r'🔀'
t_AND        = r'🔗'
t_NOT        = r'🚫'
t_EQ         = r'⚖️'
t_NEQ        = r'💔'
t_LE         = r'👈⚖️'
t_GE         = r'👉⚖️'
t_LT         = r'👈'
t_GT         = r'👉'
t_IF         = r'❓'
t_ELSE       = r'💡'
t_WHILE      = r'🔁'
t_LBRACE     = r'🧱'
t_RBRACE     = r'🛑'
t_EXIT       = r'🏁'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'

t_ignore = ' \t\r'

def t_ignore_enter(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_NUMBER(t):
    r'[0-9]+(\.[0-9]+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_STRING(t):
    r'💬[^💬]*💬'
    t.value = t.value[1:-1]
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

def t_NEWLINE(t):
    r'🔚'
    return t

def t_error(t):
    print(f"🔥 Błąd leksykalny w linii {t.lexer.lineno}: Nieznany symbol '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()
