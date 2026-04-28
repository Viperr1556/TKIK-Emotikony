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

```text
program : statements

statements : statements statement
           | statement

statement : assignment NEWLINE
          | print_stmt NEWLINE
          | function_def
          | return_stmt NEWLINE
          | expression NEWLINE
          | if_stmt
          | while_stmt
          | append_stmt NEWLINE
          | EXIT NEWLINE
          | NEWLINE

function_def : FUNC_DEF ID INPUT LPAREN params RPAREN LBRACE statements RBRACE
             | FUNC_DEF ID INPUT LPAREN RPAREN LBRACE statements RBRACE

params : params COMMA ID
       | ID

return_stmt : RETURN expression

assignment : ID ASSIGN expression

print_stmt : PRINT expression_list

expression_list : expression_list COMMA expression
                | expression

if_stmt : IF expression LBRACE statements RBRACE
        | IF expression LBRACE statements RBRACE ELSE LBRACE statements RBRACE

while_stmt : WHILE expression LBRACE statements RBRACE

append_stmt : ID APPEND expression

expression : expression PLUS expression
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

args : args COMMA expression
     | expression
```
---

## 5. Krótka instrukcja obsługi

1. Upewnij się, że w systemie zainstalowany jest Python (wersja minimum 3.10).
2. Zainstaluj wymaganą bibliotekę generującą parser PLY:
   ```bash
   pip install ply
   ```
3. Zapisz swój kod źródłowy w pliku tekstowym z rozszerzeniem `.emo` (koniecznie w kodowaniu UTF-8, ze względu na wykorzystanie symboli Emoji).
4. Uruchom interpreter z poziomu wiersza poleceń, podając ścieżkę do skryptu:
   ```bash
   python main.py skrypt.emo
   ```
---

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
