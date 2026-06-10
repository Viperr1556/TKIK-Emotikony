import ply.lex as lex

tokens = (
    # wartości i nazwy
    'ID', 'NUMBER', 'STRING', 'TRUE', 'FALSE',
    # struktura programu
    'ASSIGN', 'END', 'EXIT',
    'LBRACE', 'RBRACE', 'LPAREN', 'RPAREN', 'COMMA',
    # wejście / wyjście
    'PRINT', 'INPUT',
    # arytmetyka
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    # porównania
    'EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE',
    # logika
    'AND', 'OR', 'NOT',
    # rzutowanie typów
    'NUM_CAST',
    # sterowanie
    'IF', 'ELSE', 'WHILE',
    # listy
    'LBRACKET', 'RBRACKET', 'AT', 'LEN', 'APPEND',
    # funkcje
    'FUNC', 'CALL', 'RETURN',
)

#Tokeny proste (1 emoji = 1 token) 
t_ASSIGN    = r'📦'          # przypisanie do zmiennej (x 📦 5)
t_END       = r'🔚'          # koniec instrukcji (jak średnik `;`)
t_EXIT      = r'🏁'          # koniec programu

t_LBRACE    = r'🧱'          # początek bloku  {
t_RBRACE    = r'🛑'          # koniec bloku    }
t_LPAREN    = r'\('          # nawias zwykły   (
t_RPAREN    = r'\)'          # nawias zwykły   )
t_COMMA     = r'📍'          # separator argumentów  ,

t_PRINT     = r'📢'          # wypisz na ekran
t_INPUT     = r'📥'          # wczytaj linię od użytkownika

t_PLUS      = r'➕'
t_MINUS     = r'➖'
t_TIMES     = r'✖️?'         # ✖ z opcjonalnym selektorem wariantu (FE0F)
t_DIVIDE    = r'➗'

t_EQ        = r'⚖️?'         # ==
t_NEQ       = r'💔'          # !=
t_LT        = r'👈'          # <   (ostre)
t_GT        = r'👉'          # >   (ostre)
t_LE        = r'🔽'          # <=  (nieostre)
t_GE        = r'🔼'          # >=  (nieostre)

t_AND       = r'🔗'          # i
t_OR        = r'🔀'          # lub
t_NOT       = r'🚫'          # nie

t_NUM_CAST  = r'🔢'          # zamień tekst na liczbę

t_IF        = r'❓'
t_ELSE      = r'💡'
t_WHILE     = r'🔁'          # pętla "dopóki" 

t_LBRACKET  = r'📂'          # otwarcie listy  [
t_RBRACKET  = r'📁'          # zamknięcie listy ]
t_AT        = r'🎯'          # element listy pod indeksem
t_LEN       = r'📏'          # długość listy / tekstu
t_APPEND    = r'🖇️?'         # dopnij element na koniec listy

t_FUNC      = r'🎁'          # definicja funkcji
t_CALL      = r'📞'          # wywołanie funkcji
t_RETURN    = r'🔙'          # zwróć wartość z funkcji

t_TRUE      = r'✅'
t_FALSE     = r'❌'

# Znaki, które skaner ma po prostu pomijać (spacje, tabulatory).
t_ignore = ' \t\r'


#Tokeny złożone (reguły funkcyjne)
def t_COMMENT(t):
    r'\#.*'
    pass  # komentarz: nic nie zwracamy, więc token znika

def t_STRING(t):
    r'💬[^💬]*💬'              # tekst w cudzysłowach 💬 ... 💬
    t.value = t.value[1:-1]   # zdejmujemy znaczniki 💬 z początku i końca
    return t

def t_NUMBER(t):
    r'[0-9]+(\.[0-9]+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t  # nazwa zmiennej lub funkcji

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)   # liczymy linie do komunikatu o błędach 


#Obsługa błędów leksykalnych

def find_column(input_text, token):
    """Numer kolumny tokenu w danej linii - do czytelnych komunikatów."""
    last_newline = input_text.rfind('\n', 0, token.lexpos)
    return token.lexpos - last_newline

def t_error(t):
    column = find_column(t.lexer.lexdata, t)
    print(f"🔥 Błąd leksykalny: nieznany symbol '{t.value[0]}' "
          f"(linia {t.lexer.lineno}, kolumna {column})")
    t.lexer.skip(1)   #pominiemy zły znak i próbujemy przejść dalej 


lexer = lex.lex()
