# Sprawozdanie z projektu: EmoLang – Interpreter języka emotikonowego

**Przedmiot:** Teoria kompilacji i kompilatory  
**Temat projektu:** EmoLang – esoteryczny język programowania oparty na symbolach Unicode (Emoji)  

**Autorzy:** 
* **Bednarski Paweł** (e-mail: pbednarski@student.agh.edu.pl)  
* **Czosnek Bartłomiej** (e-mail: bczosnek@student.agh.edu.pl)  

---

# Dokumentacja Projektu: EmoLang

## 1. Założenia programu

### Ogólne cele programu
**EmoLang** to interpreter języka dziedzinowego (DSL) z kategorii *esolangs*, w którym tradycyjna składnia tekstowa została zastąpiona zestawem symboli **Unicode (Emoji)**. Celem projektu jest stworzenie kompletnego Turingowsko języka programowania, który mimo niekonwencjonalnej formy wizualnej, oferuje zaawansowane mechanizmy informatyczne, takie jak rekurencja, dynamiczne zarządzanie listami oraz izolowane zakresy zmiennych (scope).

### Charakterystyka techniczna
* **Rodzaj translatora:** Interpreter.
* **Planowany wynik działania:** Odczyt kodu źródłowego z plików `.emo`, przeprowadzenie analizy leksykalnej i składniowej, budowa drzewa AST (Abstract Syntax Tree), a następnie wykonanie instrukcji w środowisku Python 3.10+.
* **Język implementacji:** Python.
* **Sposób realizacji skanera i parsera:** Wykorzystanie generatora **PLY (Python Lex-Yacc)**. Analiza składniowa oparta jest na parserze LALR(1).

---

## 2. Stosowane pakiety i narzędzia zewnętrzne

* **PLY (Python Lex-Yacc)** – biblioteka implementująca narzędzia `lex` i `yacc` dla Pythona.
* **sys (wbudowany)** – obsługa parametrów wejściowych i strumieni systemowych.
* **Typing (wbudowany)** – zapewnienie poprawności typowania struktur drzewa AST.

---

## 3. Opis tokenów

Skaner języka EmoLang przetwarza znaki Unicode na tokeny. Poniższa tabela przedstawia kluczowe symbole:

| Kategoria | Symbol | Token (PLY) | Opis |
| :--- | :---: | :--- | :--- |
| **Identyfikatory** | `abc` | `ID` | Nazwa zmiennej lub funkcji |
| **Liczby** | `123` | `NUMBER` | Liczba (int/float) |
| **Tekst** | 💬...💬 | `STRING` | Literał tekstowy |
| **Wartości logiczne**| ✅ / ❌ | `TRUE` / `FALSE` | Prawda / Fałsz |
| **Operatory** | 📦 | `ASSIGN` | Przypisanie wartości |
| | ➕ ➖ ✖️ ➗ | `PLUS`, `MINUS` itd. | Operacje arytmetyczne |
| | ⚖️ 💔 👈 👉 | `EQ`, `NEQ`, `LT`, `GT` | Operatory porównania |
| | 🔀 🔗 🚫 | `OR`, `AND`, `NOT` | Operatory logiczne |
| **Sterowanie** | ❓ / 💡 | `IF` / `ELSE` | Instrukcja warunkowa |
| | 🔁 | `WHILE` | Pętla warunkowa |
| | 🧱 / 🛑 | `LBRACE` / `RBRACE` | Początek / Koniec bloku |
| **Funkcje** | 🎁 | `FUNC_DEF` | Definicja funkcji |
| | 🎈 | `CALL` | Wywołanie funkcji |
| | ↪️ | `RETURN` | Zwrócenie wartości |
| **Listy** | 📂 / 📁 | `LBRACKET` / `RBRACKET` | Definicja listy |
| | 🎯 | `AT` | Dostęp przez indeks |
| | 🖇️ | `APPEND` | Dodanie elementu |
| **I/O** | 📢 / 📥 | `PRINT` / `INPUT` | Wyjście / Wejście |
| | 🔚 | `NEWLINE` | Koniec instrukcji |

---

## 4. Gramatyka języka (Format Yacc)

Poniżej przedstawiono gramatykę bezkontekstową z zachowaniem poprawnej priorytetyzacji operatorów (od najsłabszych logicznych do najsilniejszych arytmetycznych).

```python
# --- Struktura programu ---
program : statements

statements : statement
           | statements statement

statement : assignment NEWLINE
          | print_stmt NEWLINE
          | function_def
          | function_call NEWLINE
          | return_stmt NEWLINE
          | if_stmt
          | while_stmt
          | list_append NEWLINE
          | exit_stmt NEWLINE
          | NEWLINE

# --- Funkcje i zasięg ---
function_def : FUNC_DEF ID INPUT params RBRACE statements LBRACE
params : ID
       | params COMMA ID
       | empty

function_call : CALL ID INPUT args RBRACE
args : expression
     | args COMMA expression
     | empty

return_stmt : RETURN expression

# --- Instrukcje sterujące ---
if_stmt : IF expression LBRACE statements RBRACE
        | IF expression LBRACE statements RBRACE ELSE LBRACE statements RBRACE

while_stmt : WHILE expression LBRACE statements RBRACE

assignment : ID ASSIGN expression

# --- Wyrażenia i Precedencja Operatorów ---
expression : expression OR and_expr
           | and_expr

and_expr : and_expr AND condition
         | condition

condition : arithmetic EQ arithmetic
          | arithmetic NEQ arithmetic
          | arithmetic LT arithmetic
          | arithmetic GT arithmetic
          | arithmetic

arithmetic : arithmetic PLUS term
           | arithmetic MINUS term
           | term

term : term MULT factor
     | term DIV factor
     | factor

factor : NOT factor
       | LPAREN expression RPAREN
       | NUMBER
       | STRING
       | ID
       | TRUE
       | FALSE
       | function_call
       | list_access
       | list_len
       | casting_op
       | input_op

# --- Operacje na listach ---
list_literal : LBRACKET expression_list RBRACKET
             | LBRACKET RBRACKET

list_access : ID AT expression
list_append : ID APPEND expression
```

---

## 5. Krótka instrukcja obsługi

1. **Wymagania wstępne:** Zainstalowany Python w wersji minimum 3.10.
2. **Instalacja zależności:** Przed uruchomieniem interpretera należy zainstalować bibliotekę PLY.
   ```bash
   pip install ply
   ```
3. **Przygotowanie skryptu:** Kod w języku EmoLang należy zapisać w pliku tekstowym z kodowaniem UTF-8 i rozszerzeniem `.emo` (np. `skrypt.emo`).
4. **Uruchomienie interpretera:** Program uruchamia się z poziomu wiersza poleceń, przekazując ścieżkę do pliku ze skryptem jako pierwszy argument:
   ```bash
   python emoti_interpreter.py skrypt.emo
   ```

---

## 6. Przykład użycia

Poniższy skrypt (`demo.emo`) prezentuje pełnię możliwości języka: inicjalizację zmiennych, pobieranie danych od użytkownika, działanie pętli warunkowej (iterowanie, rzutowanie typu i dodawanie do listy) oraz sprawdzanie warunku.

**Plik `demo.emo`:**
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
