# EmoLang — Interpreter języka opartego na Emoji

## 1. Dane studentów

| Pole | Wartość |
|---|---|
| **Imię i nazwisko** | Paweł Bednarski |
| **E-mail** | pbednarski@student.agh.edu.pl |
| **Imię i nazwisko** | Bartłomiej Czosnek |
| **E-mail** | bczosnek@student.agh.edu.pl |
| **Przedmiot** | Teoria Kompilacji i Kompilatory |

---

## 2. Założenia programu

### Ogólne cele programu

Stworzenie w pełni funkcjonalnego języka dziedzinowego (z kategorii *esolangs*), w którym tradycyjna składnia tekstowa słów kluczowych została zastąpiona symbolami Unicode (Emoji). Program pozwala na obsługę zmiennych, operacji matematycznych i logicznych, instrukcji warunkowych, pętli, struktur danych (list) oraz definiowanie i wywoływanie funkcji w izolowanych środowiskach.

### Rodzaj translatora

**Interpreter** — program analizuje plik wejściowy `.emo`, buduje drzewo składniowe (AST) i wykonuje kod, prezentując wyniki na standardowym wyjściu (konsoli).

### Planowany wynik działania

Interpreter języka EmoLang wyświetlający wyniki obliczeń i komunikaty I/O dla użytkownika na podstawie skryptu `.emo`.

### Język implementacji

**Python 3.10+**

### Sposób realizacji skanera i parsera

Wykorzystanie generatora skanerów i parserów **PLY** (Python Lex-Yacc) — implementacja narzędzi `lex`/`yacc` dla języka Python.

Wybór generatora na podstawie: [Comparison of parser generators](https://en.wikipedia.org/wiki/Comparison_of_parser_generators)

---

## 3. Pakiety zewnętrzne

- **PLY** (`ply.lex`, `ply.yacc`) — biblioteka implementująca narzędzia lex/yacc dla języka Python, użyta do analizy leksykalnej i składniowej.
- **Flask** — lekki framework webowy użyty do budowy interfejsu Web UI.

---

## 4. Opis tokenów

Skaner zamienia ciągi znaków (w tym wielobajtowe symbole Unicode) na następujące tokeny:

| Kategoria | Symbol / Format | Token (PLY) | Opis |
|---|---|---|---|
| **Typy i zmienne** | `[a-zA-Z_][a-zA-Z0-9_]*` | `ID` | Nazwa zmiennej lub funkcji |
| | `[0-9]+(\.[0-9]+)?` | `NUMBER` | Wartość liczbowa (całkowita lub zmiennoprzecinkowa) |
| | 💬 *tekst* 💬 | `STRING` | Literał tekstowy |
| | ✅ / ❌ | `TRUE` / `FALSE` | Wartości logiczne Prawda / Fałsz |
| **Konwersja typów** | 🔢 / 📉 / 🔤 | `INT_CAST` / `FLOAT_CAST` / `STR_CAST` | Rzutowanie na int / float / string |
| **Operatory arytm.** | ➕ / ➖ / ✖️ / ➗ | `PLUS` / `MINUS` / `MULTIPLY` / `DIVIDE` | Operatory arytmetyczne |
| **Operatory logiczne** | 🔀 / 🔗 / 🚫 | `OR` / `AND` / `NOT` | LUB / I / NIE |
| **Porównania** | ⚖️ / 💔 | `EQ` / `NEQ` | Równe / Różne |
| | 👈 / 👉 | `LT` / `GT` | Mniejsze / Większe |
| | 👈⚖️ / 👉⚖️ | `LE` / `GE` | Mniejsze lub równe / Większe lub równe |
| **Przypisanie** | 📦 | `ASSIGN` | Przypisanie wartości do zmiennej |
| **Listy** | 📂 / 📁 | `LBRACKET` / `RBRACKET` | Otwarcie / zamknięcie definicji listy |
| | 🎯 | `AT` | Pobranie elementu z listy pod indeksem |
| | 📏 | `LEN` | Długość listy (lub tekstu) |
| | 🖇️ | `APPEND` | Dodanie elementu na koniec listy |
| **Sterowanie** | ❓ / 💡 | `IF` / `ELSE` | Instrukcja warunkowa |
| | 🔁 | `WHILE` | Pętla warunkowa |
| | 🧱 / 🛑 | `LBRACE` / `RBRACE` | Początek / koniec bloku instrukcji |
| **Funkcje** | 🎁 | `FUNC_DEF` | Definicja funkcji |
| | 🎈 | `CALL` | Wywołanie funkcji |
| | ↪️ | `RETURN` | Zwrócenie wartości z funkcji |
| **I/O i inne** | 📢 / 📥 | `PRINT` / `INPUT` | Wyjście (print) / Wejście (input) |
| | 📍 | `COMMA` | Separator argumentów |
| | `(` / `)` | `LPAREN` / `RPAREN` | Nawiasy grupujące wyrażenia |
| | 🔚 | `NEWLINE` | Koniec linii / instrukcji |
| | 🏁 | `EXIT` | Zakończenie pracy skryptu |

---

## 5. Gramatyka formatu

Poniżej znajduje się czysta gramatyka w notacji generatora Yacc (PLY), opisująca strukturę języka (bez akcji semantycznych). Zastosowano hierarchię priorytetów operatorów w celu uniknięcia konfliktów *shift/reduce*.

```
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

/* Priorytety operatorów (od najniższego do najwyższego) */
%left OR
%left AND
%left EQ NEQ LT GT LE GE
%left PLUS MINUS
%left MULTIPLY DIVIDE
%right NOT

%%

/* ===== Korzeń gramatyki ===== */

program
    : top_statement_list
    ;

top_statement_list
    : top_statement_list top_statement
    | top_statement
    ;

/* Instrukcje dozwolone na poziomie głównym programu (bez return) */
top_statement
    : assignment NEWLINE
    | print_stmt NEWLINE
    | if_top_stmt
    | while_top_stmt
    | append_stmt NEWLINE
    | expression NEWLINE
    | function_def
    | EXIT NEWLINE
    | NEWLINE
    ;

/* ===== Definicja funkcji ===== */

function_def
    : FUNC_DEF ID INPUT LPAREN params RPAREN LBRACE func_body RBRACE
    | FUNC_DEF ID INPUT LPAREN RPAREN LBRACE func_body RBRACE
    ;

params
    : params COMMA ID
    | ID
    ;

/* ===== Ciało funkcji (może zawierać return) ===== */

func_body
    : func_statement_list
    ;

func_statement_list
    : func_statement_list func_statement
    | func_statement
    ;

/* Instrukcje dozwolone wewnątrz funkcji (z return) */
func_statement
    : assignment NEWLINE
    | print_stmt NEWLINE
    | if_func_stmt
    | while_func_stmt
    | append_stmt NEWLINE
    | expression NEWLINE
    | return_stmt NEWLINE
    | NEWLINE
    ;

return_stmt
    : RETURN expression
    ;

/* ===== Instrukcja warunkowa (poziom główny) ===== */

if_top_stmt
    : IF expression LBRACE top_statement_list RBRACE
    | IF expression LBRACE top_statement_list RBRACE ELSE LBRACE top_statement_list RBRACE
    ;

/* ===== Pętla while (poziom główny) ===== */

while_top_stmt
    : WHILE expression LBRACE top_statement_list RBRACE
    ;

/* ===== Instrukcja warunkowa (wewnątrz funkcji) ===== */

if_func_stmt
    : IF expression LBRACE func_statement_list RBRACE
    | IF expression LBRACE func_statement_list RBRACE ELSE LBRACE func_statement_list RBRACE
    ;

/* ===== Pętla while (wewnątrz funkcji) ===== */

while_func_stmt
    : WHILE expression LBRACE func_statement_list RBRACE
    ;

/* ===== Wspólne instrukcje ===== */

assignment
    : ID ASSIGN expression
    ;

print_stmt
    : PRINT expression_list
    ;

append_stmt
    : ID APPEND expression
    ;

/* ===== Wyrażenia ===== */

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

expression_list
    : expression_list COMMA expression
    | expression
    ;

args
    : args COMMA expression
    | expression
    ;

%%
```

---

## 6. Krótka instrukcja obsługi

**Wymagania wstępne:** Python 3.10 lub nowszy.

**Instalacja zależności:**
```
pip install ply flask
```

**Zapisz kod** w pliku `.emo` w kodowaniu UTF-8 (wymagane ze względu na Emoji).

### Tryb konsolowy

```
python main.py skrypt.emo
```

### Tryb Web UI (zalecany)

Projekt zawiera interfejs webowy oparty na Flask umożliwiający wybór pliku `.emo`, podawanie danych wejściowych i podgląd wyników w przeglądarce.

```
python web_ui.py
```

Następnie otwórz w przeglądarce: `http://127.0.0.1:5000`

---

## 7. Przykład użycia

Plik `demo.emo` — pobieranie danych od użytkownika, pętla, lista, instrukcja warunkowa:

```
# --- Inicjalizacja ---
📢 💬 Witaj w EmoLang! Ile liczb chcesz zapisac w liscie? 💬 🔚
limit 📦 🔢 ( 📥 ( ) ) 🔚

liczby 📦 📂 📁 🔚
suma 📦 0 🔚
i 📦 0 🔚

# --- Pobieranie danych w petli ---
🔁 i 👈 limit 🧱
    📢 💬 Podaj liczbe: 💬 📍 i ➕ 1 🔚
    n 📦 🔢 ( 📥 ( ) ) 🔚
    liczby 🖇️ n 🔚
    suma 📦 suma ➕ n 🔚
    i 📦 i ➕ 1 🔚
🛑

# --- Wyniki ---
📢 💬 Twoja lista: 💬 📍 liczby 🔚
📢 💬 Dlugosc listy: 💬 📍 📏 liczby 🔚
📢 💬 Suma elementow: 💬 📍 suma 🔚

# --- Warunek ---
❓ suma 👉 50 🧱
    📢 💬 Wynik jest wysoki! 💬 🔚
🛑 💡 🧱
    📢 💬 Wynik jest niski. 💬 🔚
🛑

🏁 🔚
```

Przykład z funkcją zwracającą wartość:

```
🎁 silnia 📥 ( n ) 🧱
    ❓ n ⚖️ 0 🧱
        ↪️ 1 🔚
    🛑
    ↪️ n ✖️ 🎈 silnia 📥 ( n ➖ 1 ) 🔚
🛑

wynik 📦 🎈 silnia 📥 ( 5 ) 🔚
📢 💬 Silnia z 5 to: 💬 📍 wynik 🔚
🏁 🔚
```
