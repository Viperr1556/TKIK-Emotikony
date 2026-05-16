## 1. Założenia programu

### Ogólne cele programu
Stworzenie w pełni funkcjonalnego języka dziedzinowego (z kategorii *esolangs*), w którym tradycyjna składnia tekstowa słów kluczowych została zastąpiona symbolami Unicode (Emoji). Program pozwala na obsługę zmiennych, operacji matematycznych i logicznych, instrukcji warunkowych, pętli, struktur danych (list) oraz definiowanie i wywoływanie funkcji w izolowanych środowiskach.

### Szczegóły techniczne
* **Rodzaj translatora:** Interpreter.
* **Planowany wynik działania programu:** Interpreter analizuje plik wejściowy `.emo`, buduje drzewo składniowe (AST) i wykonuje kod, prezentując na standardowym wyjściu (konsoli) wyniki działania skryptu oraz komunikaty I/O dla użytkownika.
* **Język implementacji:** Python (3.10+).
* **Sposób realizacji skanera i parsera:** Wykorzystanie generatora skanerów i parserów **PLY** (Python Lex-Yacc).

---

## 2. Pakiety zewnętrzne

* **PLY (ply.lex, ply.yacc)** – zewnętrzna biblioteka implementująca narzędzia lex/yacc dla języka Python, użyta do analizy leksykalnej i składniowej.

---

## 3. Opis tokenów

Skaner zamienia ciągi znaków (w tym wielobajtowe symbole Unicode) na następujące tokeny:

| Kategoria | Symbol / Format | Token (PLY) | Opis |
| :--- | :---: | :--- | :--- |
| **Typy i zmienne** | `[a-zA-Z_]...` | `ID` | Nazwa zmiennej lub funkcji |
| | `[0-9]+...` | `NUMBER` | Wartość liczbowa (całkowita lub zmiennoprzecinkowa) |
| | 💬 *tekst* 💬 | `STRING` | Literał tekstowy |
| | ✅ / ❌ | `TRUE` / `FALSE` | Wartości logiczne Prawda / Fałsz |
| **Konwersja typów** | 🔢 / 📉 / 🔤 | `INT_CAST` / `FLOAT_CAST` / `STR_CAST` | Rzutowanie na int / float / string |
| **Operatory** | 📦 | `ASSIGN` | Przypisanie wartości do zmiennej |
| | ➕ / ➖ / ✖️ / ➗ | `PLUS` / `MINUS` / `MULTIPLY` / `DIVIDE` | Operatory arytmetyczne |
| | 🔀 / 🔗 / 🚫 | `OR` / `AND` / `NOT` | Operatory logiczne (LUB, I, NIE) |
| **Porównania** | ⚖️ / 💔 | `EQ` / `NEQ` | Równe / Różne |
| | 👈 / 👉 | `LT` / `GT` | Mniejsze / Większe |
| | 👈⚖️ / 👉⚖️ | `LE` / `GE` | Mniejsze lub równe / Większe lub równe |
| **Listy**| 📂 / 📁 | `LBRACKET` / `RBRACKET` | Otwarcie / zamknięcie definicji listy |
| | 🎯 | `AT` | Pobranie elementu z listy pod indeksem |
| | 📏 | `LEN` | Długość listy (lub tekstu) |
| | 🖇️ | `APPEND` | Dodanie elementu na koniec listy |
| **Sterowanie** | ❓ / 💡 | `IF` / `ELSE` | Instrukcja warunkowa |
| | 🔁 | `WHILE` | Pętla warunkowa |
| | 🧱 / 🛑 | `LBRACE` / `RBRACE` | Początek / koniec bloku instrukcji |
| **Funkcje** | 🎁 | `FUNC_DEF` | Definicja funkcji |
| | 🎈 | `CALL` | Wywołanie funkcji |
| | ↪️ | `RETURN` | Zwrócenie wartości z funkcji |
| **I/O i znaki** | 📢 / 📥 | `PRINT` / `INPUT` | Wyjście (print) / Wejście (input) |
| | 📍 | `COMMA` | Separator argumentów (przecinek) |
| | `(` / `)` | `LPAREN` / `RPAREN` | Nawiasy grupujące wyrażenia |
| | 🔚 | `NEWLINE` | Koniec linii / instrukcji |
| | 🏁 | `EXIT` | Zakończenie pracy skryptu |

---

## 4. Gramatyka formatu

Poniżej znajduje się czysta gramatyka w notacji generatora Yacc (PLY), opisująca strukturę języka (bez akcji semantycznych). Zastosowano hierarchię priorytetów operatorów, aby zapobiec konfliktom *shift/reduce*.

```yacc
%token FUNC_DEF RETURN IF ELSE WHILE PRINT INPUT
%token TRUE FALSE EXIT
%token INT_CAST FLOAT_CAST STR_CAST LEN
%token APPEND CALL
%token ID NUMBER STRING
%token PLUS MINUS MULTIPLY DIVIDE
%token EQ NEQ LT GT LE GE
%token AND OR NOT
%token ASSIGN
%token LPAREN RPAREN
%token LBRACE RBRACE
%token LBRACKET RBRACKET
%token COMMA NEWLINE
%token AT

/* Priorytety operatorów */
%left OR
%left AND
%left EQ NEQ LT GT LE GE
%left PLUS MINUS
%left MULTIPLY DIVIDE
%right NOT

%%

/* Korzeń gramatyki */
program
    : statements
    ;

/* Lista instrukcji */
statements
    : statements statement
    | statement
    ;

/* Instrukcje */
statement
    : assignment NEWLINE
    | print_stmt NEWLINE
    | function_def
    | return_stmt NEWLINE
    | expression NEWLINE
    | if_stmt
    | while_stmt
    | append_stmt NEWLINE
    | EXIT NEWLINE
    | NEWLINE
    ;

/* Definicja funkcji */
function_def
    : FUNC_DEF ID INPUT LPAREN params RPAREN LBRACE statements RBRACE
    | FUNC_DEF ID INPUT LPAREN RPAREN LBRACE statements RBRACE
    ;

/* Parametry funkcji */
params
    : params COMMA ID
    | ID
    ;

/* Return */
return_stmt
    : RETURN expression
    ;

/* Przypisanie */
assignment
    : ID ASSIGN expression
    ;

/* Print */
print_stmt
    : PRINT expression_list
    ;

/* Lista wyrażeń */
expression_list
    : expression_list COMMA expression
    | expression
    ;

/* Instrukcja IF */
if_stmt
    : IF expression LBRACE statements RBRACE
    | IF expression LBRACE statements RBRACE ELSE LBRACE statements RBRACE
    ;

/* Pętla WHILE */
while_stmt
    : WHILE expression LBRACE statements RBRACE
    ;

/* Dodawanie do listy */
append_stmt
    : ID APPEND expression
    ;

/* Wyrażenia */
expression
    : expression PLUS expression
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
    | expression OR expression
    | NOT expression

    | INT_CAST LPAREN expression RPAREN
    | FLOAT_CAST LPAREN expression RPAREN
    | STR_CAST LPAREN expression RPAREN

    | LBRACKET expression_list RBRACKET
    | LBRACKET RBRACKET

    | expression AT expression
    | LEN expression

    | CALL ID INPUT LPAREN args RPAREN
    | CALL ID INPUT LPAREN RPAREN

    | INPUT LPAREN RPAREN

    | LPAREN expression RPAREN

    | NUMBER
    | STRING
    | TRUE
    | FALSE
    | ID
    ;

/* Argumenty funkcji */
args
    : args COMMA expression
    | expression
    ;

%%
```

---

## 5. Krótka instrukcja obsługi

1. Upewnij się, że w systemie zainstalowany jest Python (wersja minimum 3.10).

2. Zainstaluj wymagane biblioteki:

   ```bash
   pip install ply flask
   ```

3. Zapisz swój kod źródłowy w pliku tekstowym z rozszerzeniem `.emo`
   (koniecznie w kodowaniu UTF-8, ze względu na wykorzystanie symboli Emoji).

4. Interpreter można uruchomić na dwa sposoby:

### Tryb konsolowy

Uruchom interpreter z poziomu wiersza poleceń, podając ścieżkę do skryptu:

```bash
python main.py skrypt.emo
```

### Tryb Web UI (zalecany)

Projekt zawiera prosty interfejs webowy oparty na Flask, umożliwiający:

* wybór plików `.emo` z poziomu przeglądarki,
* uruchamianie programów bez używania terminala,
* podawanie danych wejściowych dla funkcji `input()`,
* podgląd wyników interpretera w czasie rzeczywistym.

Uruchom interfejs poleceniem:

```bash
python web_ui.py
```

Następnie otwórz w przeglądarce:

```text
http://127.0.0.1:5000
```

Po uruchomieniu strony można wybierać przykładowe programy `.emo`,
wprowadzać dane wejściowe oraz obserwować wynik działania interpretera.


## 6. Przykład użycia

Kod w pliku `demo.emo`, prezentujący pobieranie danych od użytkownika, rzutowanie typów, działanie pętli, modyfikację listy oraz instrukcję warunkową:

```text
# --- Inicjalizacja programu ---
📢 💬 Witaj w EmoLang! Ile liczb chcesz zapisac w liscie? 💬 🔚
limit 📦 🔢 ( 📥 ( ) ) 🔚

liczby 📦 📂 📁 🔚
suma 📦 0 🔚
i 📦 0 🔚

# --- Pobieranie danych w petli ---
🔁 i 👈 limit 🧱
    📢 💬 Podaj liczbe 💬 📍 i ➕ 1 🔚
    n 📦 🔢 ( 📥 ( ) ) 🔚
    
    liczby 🖇️ n 🔚
    suma 📦 suma ➕ n 🔚
    i 📦 i ➕ 1 🔚
🛑

# --- Analiza danych ---
📢 💬 Twoja lista: 💬 📍 liczby 🔚
📢 💬 Dlugosc listy: 💬 📍 📏 liczby 🔚
📢 💬 Suma elementow: 💬 📍 suma 🔚

# --- Warunek logiczny ---
❓ suma 👉 50 🧱
    📢 💬 Wynik jest wysoki! 💬 🔚
🛑 💡 🧱
    📢 💬 Wynik jest niski. 💬 🔚
🛑

🏁 🔚
```
