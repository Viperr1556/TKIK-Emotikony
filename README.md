# Sprawozdanie z projektu: EmoLang – Interpreter języka emotikonowego

**Przedmiot:** Teoria kompilacji i kompilatory  
**Temat projektu:** EmoLang – esoteryczny język programowania oparty na symbolach Unicode (Emoji)  

**Autorzy:** 
* **Bednarski Paweł** (e-mail: pbednarski@student.agh.edu.pl)  
* **Czosnek Bartłomiej** (e-mail: bczosnek@student.agh.edu.pl)  

---

## 1. Założenia programu

### Ogólne cele programu
**EmoLang** to interpreter języka dziedzinowego (DSL) z kategorii *esolangs*, w którym tradycyjna składnia tekstowa została zastąpiona zestawem symboli **Unicode (Emoji)**. Celem projektu jest stworzenie w pełni funkcjonalnego języka programowania opartego na piktogramach, obsługującego operacje arytmetyczne, logiczne, struktury sterujące (pętle, instrukcje warunkowe) oraz podstawowe struktury danych (listy).

### Charakterystyka techniczna
* **Rodzaj translatora:** Interpreter.
* **Planowany wynik działania:** Odczyt kodu źródłowego z plików z rozszerzeniem `.emo`, budowa drzewa składniowego (AST), a następnie bezpośrednie wykonanie instrukcji w środowisku Python z interakcją poprzez standardowe wejście/wyjście (konsolę).
* **Język implementacji:** Python 3.10+.
* **Sposób realizacji skanera i parsera:** Wykorzystanie generatora skanerów i parserów **PLY** (Python Lex-Yacc). Faza analizy leksykalnej identyfikuje poszczególne emoji, a parser LALR(1) buduje z nich drzewo AST w oparciu o zdefiniowaną gramatykę.

---

## 2. Stosowane pakiety i narzędzia zewnętrzne

Projekt został zrealizowany z naciskiem na minimalizację zależności zewnętrznych. Głównym i jedynym wymaganym pakietem zewnętrznym jest:
* **PLY (Python Lex-Yacc)** – biblioteka implementująca narzędzia generacji analizatorów leksykalnych (lex) oraz składniowych (yacc) dla języka Python. Posłużyła do stworzenia modułów skanera i parsera.
* **Moduł `sys` (wbudowany)** – używany do obsługi argumentów wiersza poleceń (przekazywanie ścieżki do pliku źródłowego).

---

## 3. Opis tokenów

Skaner języka EmoLang zamienia ciągi znaków (w tym piktogramy Unicode) na odpowiednie tokeny analizowane przez parser. Zestawienie tokenów przedstawia poniższa tabela:

| Kategoria | Symbol w kodzie | Token (PLY) | Opis / Działanie |
| :--- | :---: | :--- | :--- |
| **Identyfikatory** | `abc`, `wynik` | `ID` | Nazwa zmiennej (litery, cyfry, `_`) |
| **Liczby** | `123`, `3.14` | `NUMBER` | Liczba całkowita lub zmiennoprzecinkowa |
| **Tekst** | 💬...💬 | `STRING` | Literał tekstowy ograniczony dymkami |
| **Wartości logiczne**| ✅ / ❌ | `TRUE` / `FALSE` | Prawda / Fałsz |
| **Rzutowanie typu** | 🔢 | `INT_CAST` | Konwersja na liczbę całkowitą |
| | 📉 | `FLOAT_CAST` | Konwersja na liczbę zmiennoprzecinkową |
| | 🔤 | `STR_CAST` | Konwersja na typ tekstowy |
| **Operacje na Listach**| 📂 / 📁 | `LBRACKET` / `RBRACKET` | Otwarcie / zamknięcie definicji listy |
| | 🎯 | `AT` | Dostęp do elementu przez indeks |
| | 📏 | `LEN` | Pobranie długości listy lub tekstu |
| | 🖇️ | `APPEND` | Dodanie elementu na koniec listy |
| **Wejście / Wyjście** | 📢 | `PRINT` | Wypisanie danych na standardowe wyjście |
| | 📥 | `INPUT` | Pobranie danych ze standardowego wejścia |
| | 📍 | `COMMA` | Separator argumentów / elementów |
| **Operatory** | 📦 | `ASSIGN` | Przypisanie wartości do zmiennej |
| | ➕ ➖ ✖️ ➗ | `PLUS`, `MINUS`, `MULT`, `DIV` | Podstawowe operatory arytmetyczne |
| | 🔀 🔗 🚫 | `OR`, `AND`, `NOT` | Operatory logiczne |
| | ⚖️ 💔 👈 👉 | `EQ`, `NEQ`, `LT`, `GT` | Operatory porównania (==, !=, <, >) |
| **Sterowanie** | ❓ / 💡 | `IF` / `ELSE` | Instrukcja warunkowa |
| | 🔁 | `WHILE` | Pętla warunkowa |
| | 🧱 / 🛑 | `LBRACE` / `RBRACE` | Początek i koniec bloku instrukcji |
| | 🔚 | `NEWLINE` | Znak nowej linii / koniec instrukcji |
| | 🏁 | `EXIT` | Zakończenie pracy programu |
| **Nawiasy** | `(` / `)` | `LPAREN` / `RPAREN` | Nawiasy grupujące w wyrażeniach |

---

## 4. Gramatyka języka (Format Yacc)

Poniżej przedstawiono bezkontekstową gramatykę języka w notacji używanej przez generator parserów PLY (Yacc), bez definicji akcji (czysta struktura).

```python
# --- Sekcja: Struktura programu ---
program : statements

statements : statement
           | statements statement

statement : assignment NEWLINE
          | print_stmt NEWLINE
          | if_stmt
          | while_stmt
          | list_append NEWLINE
          | exit_stmt NEWLINE
          | NEWLINE

assignment : ID ASSIGN expression

list_append : ID APPEND expression

print_stmt : PRINT expression_list

expression_list : expression
                | expression_list COMMA expression

# --- Sekcja: Przepływ sterowania ---
if_stmt : IF expression LBRACE statements RBRACE
        | IF expression LBRACE statements RBRACE ELSE LBRACE statements RBRACE

while_stmt : WHILE expression LBRACE statements RBRACE

exit_stmt : EXIT

# --- Sekcja: Wyrażenia i Hierarchia Operatorów ---
expression : expression PLUS term
           | expression MINUS term
           | expression OR term
           | term

term : term MULTIPLY factor
     | term DIVIDE factor
     | term AND factor
     | factor

factor : factor EQ comparison
       | factor NEQ comparison
       | factor LT comparison
       | factor GT comparison
       | factor LE comparison
       | factor GE comparison
       | comparison

# --- Sekcja: Operandy i funkcje wbudowane ---
comparison : LPAREN expression RPAREN
           | NOT comparison
           | NUMBER
           | STRING
           | ID
           | TRUE
           | FALSE
           | list_literal
           | list_access
           | list_len
           | casting_op
           | input_op

list_literal : LBRACKET expression_list RBRACKET
             | LBRACKET RBRACKET

list_access : ID AT expression

list_len : LEN ID

casting_op : INT_CAST LPAREN expression RPAREN
           | FLOAT_CAST LPAREN expression RPAREN
           | STR_CAST LPAREN expression RPAREN

input_op : INPUT LPAREN expression RPAREN
         | INPUT LPAREN RPAREN
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
