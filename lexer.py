import ply.lex as lex

# --- 1. Lista wszystkich tokenów (musi pokrywać się z Yacc) ---
tokens = (
    # Typy danych i identyfikatory
    'ID', 'NUMBER', 'STRING', 'TRUE', 'FALSE',
    
    # Rzutowanie
    'INT_CAST', 'FLOAT_CAST', 'STR_CAST',
    
    # Operacje na listach
    'LBRACKET', 'RBRACKET', 'AT', 'LEN', 'APPEND',
    
    # Wejście / Wyjście
    'PRINT', 'INPUT', 'COMMA',
    
    # Operatory arytmetyczne i przypisania
    'ASSIGN', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE',
    
    # Operatory logiczne
    'OR', 'AND', 'NOT',
    
    # Operatory porównania
    'EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE',
    
    # Sterowanie i struktura
    'IF', 'ELSE', 'WHILE', 'LBRACE', 'RBRACE',
    'NEWLINE', 'EXIT',
    
    # Nawiasy grupujące
    'LPAREN', 'RPAREN'
)

# --- 2. Proste tokeny (Reguły jako ciągi znaków) ---
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

t_ASSIGN     = r'📦'
t_PLUS       = r'➕'
t_MINUS      = r'➖'
t_MULTIPLY   = r'✖️'
t_DIVIDE     = r'➗'

t_OR         = r'🔀'
t_AND        = r'🔗'
t_NOT        = r'🚫'

t_EQ         = r'⚖️'
t_NEQ        = r'💔'
t_LT         = r'👈'
t_GT         = r'👉'
t_LE         = r'<='  # Brak w tabeli, dodane dla spójności z gramatyką
t_GE         = r'>='  # Brak w tabeli, dodane dla spójności z gramatyką

t_IF         = r'❓'
t_ELSE       = r'💡'
t_WHILE      = r'🔁'
t_LBRACE     = r'🧱'
t_RBRACE     = r'🛑'

t_NEWLINE    = r'🔚'
t_EXIT       = r'🏁'

t_LPAREN     = r'\('
t_RPAREN     = r'\)'


# --- 3. Tokeny wymagające dodatkowej logiki (Funkcje) ---

def t_STRING(t):
    r'💬.*?💬'
    # Usuwamy dymki 💬 z początku i końca, zostawiając sam tekst
    t.value = t.value[1:-1]
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    # Sprawdzamy czy to float czy int na podstawie kropki
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Zmienne nie mogą nadpisywać słów kluczowych, ale tutaj słowa 
    # kluczowe to emoji, więc klasyczne nazwy (np. 'liczba') są bezpieczne.
    return t

# --- 4. Znaki ignorowane i komentarze ---

# Ignoruj spacje i tabulacje
t_ignore = ' \t'

# Komentarze (od '#' do końca linii) - zgodnie z plikiem demo.emo
def t_ignore_COMMENT(t):
    r'\#.*'
    pass

# Obsługa klasycznych znaków nowej linii (zliczanie linii)
# Uwaga: dla parsera znaczenie ma '🔚', klasyczny '\n' jest ignorowany
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# --- 5. Obsługa błędów ---
def t_error(t):
    print(f"[Błąd leksykalny] Nieznany znak/emotikona: '{t.value[0]}' w linii {t.lexer.lineno}")
    t.lexer.skip(1)

# --- 6. Inicjalizacja lexera ---
lexer = lex.lex()

# --- BLOK TESTOWY ---
# Uruchomi się tylko jeśli uruchomisz bezpośrednio ten plik
if __name__ == "__main__":
    kod_testowy = """
    # To jest test lexera
    liczba 📦 10 🔚
    📢 💬 Wynik: 💬 📍 liczba 🔚
    """
    
    print("Rozpoczynam analizę leksykalną...")
    lexer.input(kod_testowy)
    for tok in lexer:
        print(f"Token: {tok.type:10} | Wartość: {tok.value}")
