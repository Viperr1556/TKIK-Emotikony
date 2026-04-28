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

## 3. Opis tokenów (Pełna Specyfikacja)

Skaner języka EmoLang przetwarza znaki Unicode oraz literały na tokeny. Został skonfigurowany tak, aby poprawnie obsługiwać symbole wielobajtowe oraz złożone operatory porównania.

| Kategoria | Symbol | Token (PLY) | Opis |
| :--- | :---: | :--- | :--- |
| **Identyfikatory** | `abc` | `ID` | Nazwa zmiennej lub funkcji |
| **Liczby** | `123.4` | `NUMBER` | Literał liczbowy (int/float) |
| **Tekst** | 💬...💬 | `STRING` | Literał tekstowy |
| **Logika** | ✅ / ❌ | `TRUE` / `FALSE` | Prawda / Fałsz |
| **Funkcje** | 🎁 | `FUNC_DEF` | Definicja nowej funkcji |
| | 🎈 | `CALL` | Wywołanie funkcji |
| | ↪️ | `RETURN` | Zwrócenie wartości z funkcji |
| **Rzutowanie** | 🔢 / 📉 / 🔤 | `INT_CAST` / `FLOAT_CAST` / `STR_CAST` | Konwersja typu (int/float/string) |
| **Operatory** | 📦 | `ASSIGN` | Przypisanie wartości |
| | ➕ / ➖ | `PLUS` / `MINUS` | Dodawanie / Odejmowanie |
| | ✖️ / ➗ | `MULTIPLY` / `DIVIDE` | Mnożenie / Dzielenie |
| | 🔀 / 🔗 / 🚫 | `OR` / `AND` / `NOT` | Operatory logiczne |
| **Porównania** | ⚖️ / 💔 | `EQ` / `NEQ` | Równe / Różne |
| | 👈 / 👉 | `LT` / `GT` | Mniejsze / Większe |
| | 👈⚖️ / 👉⚖️ | `LE` / `GE` | Mniejsze równe / Większe równe |
| **Listy** | 📂 / 📁 | `LBRACKET` / `RBRACKET` | Definicja listy |
| | 🎯 | `AT` | Dostęp do elementu przez indeks |
| | 📏 | `LEN` | Pobranie długości listy lub tekstu |
| | 🖇️ | `APPEND` | Dodanie elementu na koniec listy |
| **Sterowanie** | ❓ / 💡 | `IF` / `ELSE` | Instrukcja warunkowa |
| | 🔁 | `WHILE` | Pętla warunkowa |
| | 🧱 / 🛑 | `LBRACE` / `RBRACE` | Początek i koniec bloku kodu |
| **I/O i Inne** | 📢 / 📥 | `PRINT` / `INPUT` | Wyjście / Wejście danych |
| | 📍 | `COMMA` | Separator argumentów / elementów |
| | 🔚 | `NEWLINE` | Koniec instrukcji |
| | 🏁 | `EXIT` | Zakończenie pracy programu |
| | `(` / `)` | `LPAREN` / `RPAREN` | Nawiasy grupujące |

---

## 4. Gramatyka języka (Format Yacc)

Poniższa gramatyka definiuje strukturę języka EmoLang, uwzględniając priorytety operatorów oraz zagnieżdżone struktury sterujące i funkcje.

```python
# --- Sekcja: Struktura główna ---
program : statements

statements : statements statement
           | statement

statement : assignment NEWLINE
          | print_stmt NEWLINE
          | function_def
          | return_stmt NEWLINE
          | if_stmt
          | while_stmt
          | append_stmt NEWLINE
          | EXIT NEWLINE
          | NEWLINE

# --- Sekcja: Funkcje (Zakres lokalny) ---
function_def : FUNC_DEF ID INPUT params RBRACE statements LBRACE
             | FUNC_DEF ID INPUT RBRACE statements LBRACE

params : params COMMA ID
       | ID

function_call : CALL ID INPUT args RBRACE
              | CALL ID INPUT RBRACE

args : args COMMA expression
     | expression

return_stmt : RETURN expression

# --- Sekcja: Przypisanie i I/O ---
assignment : ID ASSIGN expression

print_stmt : PRINT expression_list

expression_list : expression_list COMMA expression
                | expression

# --- Sekcja: Przepływ sterowania ---
if_stmt : IF expression LBRACE statements RBRACE
        | IF expression LBRACE statements RBRACE ELSE LBRACE statements RBRACE

while_stmt : WHILE expression LBRACE statements RBRACE

# --- Sekcja: Wyrażenia (Hierarchia Operatorów) ---
expression : expression OR and_expr
           | and_expr

and_expr : and_expr AND condition
         | condition

condition : arithmetic EQ arithmetic
          | arithmetic NEQ arithmetic
          | arithmetic LT arithmetic
          | arithmetic GT arithmetic
          | arithmetic LE arithmetic
          | arithmetic GE arithmetic
          | arithmetic

arithmetic : arithmetic PLUS term
           | arithmetic MINUS term
           | term

term : term MULTIPLY factor
     | term DIVIDE factor
     | factor

factor : NOT factor
       | casting_op
       | list_op
       | atom

# --- Sekcja: Operandy i Typy Złożone ---
casting_op : INT_CAST LPAREN expression RPAREN
           | FLOAT_CAST LPAREN expression RPAREN
           | STR_CAST LPAREN expression RPAREN

list_op : LBRACKET expression_list RBRACKET
        | LBRACKET RBRACKET
        | ID AT expression
        | LEN ID

append_stmt : ID APPEND expression

atom : NUMBER
     | STRING
     | ID
     | TRUE
     | FALSE
     | function_call
     | INPUT LPAREN RPAREN
     | LPAREN expression RPAREN
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
