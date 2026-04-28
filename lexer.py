import ply.lex as lex

# Wszystkie tokeny zdefiniowane w dokumentacji EmoLang
tokens = (
    'ID', 'NUMBER', 'STRING',
    'TRUE', 'FALSE',
    'ASSIGN', 'PLUS', 'MINUS', 'MULT', 'DIV',
    'EQ', 'NEQ', 'LT', 'GT',
    'OR', 'AND', 'NOT',
    'IF', 'ELSE', 'WHILE',
    'LBRACE', 'RBRACE',
    'FUNC_DEF', 'CALL', 'RETURN',
    'LBRACKET', 'RBRACKET', 'AT', 'APPEND',
    'PRINT', 'INPUT', 'COMMA',
    'NEWLINE', 'LPAREN', 'RPAREN',
    'INT_CAST', 'FLOAT_CAST', 'STR_CAST', 'LEN',
    'EXIT'
)

# Definicje prostych tokenów (Emoji i symbole)
t_ASSIGN    = r'📦'
t_PLUS      = r'➕'
t_MINUS     = r'➖'
t_MULT      = r'✖️'
t_DIV       = r'➗'
t_EQ        = r'⚖️'
t_NEQ       = r'💔'
t_LT        = r'👈'
t_GT        = r'👉'
t_OR        = r'🔀'
t_AND       = r'🔗'
t_NOT       = r'🚫'
t_IF        = r'❓'
t_ELSE      = r'💡'
t_WHILE     = r'🔁'
t_LBRACE    = r'🧱'
t_RBRACE    = r'🛑'
t_FUNC_DEF  = r'🎁'
t_CALL      = r'🎈'
t_RETURN    = r'↪️'
t_LBRACKET  = r'📂'
t_RBRACKET  = r'📁'
t_AT        = r'🎯'
t_APPEND    = r'🖇️'
t_PRINT     = r'📢'
t_INPUT     = r'📥'
t_COMMA     = r'📍'
t_TRUE      = r'✅'
t_FALSE     = r'❌'
t_INT_CAST  = r'🔢'
t_FLOAT_CAST= r'📉'
t_STR_CAST  = r'🔤'
t_LEN       = r'📏'
t_EXIT      = r'🏁'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'

# Ignorowane znaki (spacje i taby)
t_ignore = ' \t'

# Obsługa komentarzy (wszystko po # do końca linii jest ignorowane)
def t_COMMENT(t):
    r'\#.*'
    pass

# Obsługa ID (nazwy zmiennych/funkcji)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Obsługa liczb (całkowite i zmiennoprzecinkowe)
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Obsługa stringów (tekst w dymkach)
def t_STRING(t):
    r'💬[^💬]*💬'
    t.value = t.value[1:-1] # Usuwa symbole 💬 z początku i końca
    return t

# Obsługa końca instrukcji (nowa linia)
def t_NEWLINE(t):
    r'🔚'
    t.lexer.lineno += 1
    return t

# Obsługa błędów leksykalnych
def t_error(t):
    print(f"🔥 Błąd leksykalny! Nieznany symbol: '{t.value[0]}' w linii {t.lexer.lineno}")
    t.lexer.skip(1)

# Inicjalizacja leksera
lexer = lex.lex()
