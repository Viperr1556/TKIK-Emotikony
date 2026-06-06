# EmoLang

Język programowania z kategorii *esolang*, w którym słowa kluczowe zastąpiono
symbolami Unicode (emoji). Realizacja: **interpreter** typu tree-walking
(PLY = lex + yacc, Python).

---

## 1. Dane studentów

- Bartłomiej Czosnek
- Paweł Bednarski

Przedmiot: Teoria Kompilacji i Kompilatory.

## 2. Dane kontaktowe

- bczosnek@student.agh.edu.pl
- pbednarski@student.agh.edu.pl

---

## 3. Założenia programu

**Ogólne cele.** Mały, kompletny język programowania o składni emoji,
obsługujący zmienne, typy (liczby, tekst, wartości logiczne, listy),
arytmetykę, porównania i logikę, rzutowanie typów, instrukcję warunkową,
pętlę `while`, listy
(indeksowanie, długość, dopisywanie), funkcje (parametry, wartość zwracana,
rekurencja) oraz wejście/wyjście.

**Rodzaj translatora.** Interpreter (tree-walking). Program jest analizowany
leksykalnie i składniowo do postaci drzewa składniowego (AST), które jest
następnie wykonywane bezpośrednio. Nie powstaje kod pośredni ani kod w innym
języku — nie jest to kompilator ani transpiler.

**Planowany wynik działania.** Wykonanie skryptu `.emo` i wypisanie na
standardowe wyjście wyników obliczeń oraz komunikatów I/O.

**Język implementacji.** Python 3.10+.

**Sposób realizacji skanera i parsera.** Generator **PLY** (Python Lex-Yacc):
`ply.lex` buduje skaner z wyrażeń regularnych, `ply.yacc` generuje parser
**LALR(1)** z reguł gramatyki. Wybór generatora na podstawie:
[Comparison of parser generators](https://en.wikipedia.org/wiki/Comparison_of_parser_generators).

---

## 4. Opis tokenów

Emoji występują wyłącznie w skanerze; dalsze warstwy operują na nazwach
tokenów. Jeden symbol = jeden token.

| Symbol | Token | Znaczenie |
| --- | --- | --- |
| `[a-zA-Z_][a-zA-Z0-9_]*` | `ID` | identyfikator |
| `[0-9]+(\.[0-9]+)?` | `NUMBER` | liczba (int/float) |
| 💬…💬 | `STRING` | literał tekstowy |
| ✅ / ❌ | `TRUE` / `FALSE` | wartości logiczne |
| 📦 | `ASSIGN` | przypisanie |
| 🔚 | `END` | koniec instrukcji prostej |
| 🏁 | `EXIT` | koniec programu |
| 🧱 / 🛑 | `LBRACE` / `RBRACE` | blok `{` / `}` |
| ( / ) | `LPAREN` / `RPAREN` | nawiasy |
| 📍 | `COMMA` | separator |
| 📢 / 📥 | `PRINT` / `INPUT` | wyjście / wejście |
| ➕ ➖ ✖️ ➗ | `PLUS` `MINUS` `TIMES` `DIVIDE` | arytmetyka |
| ⚖️ / 💔 | `EQ` / `NEQ` | `==` / `!=` |
| 👈 / 👉 | `LT` / `GT` | `<` / `>` |
| 🔽 / 🔼 | `LE` / `GE` | `<=` / `>=` |
| 🔗 🔀 🚫 | `AND` `OR` `NOT` | logika |
| 🔢 | `NUM_CAST` | rzutowanie tekstu na liczbę |
| ❓ / 💡 | `IF` / `ELSE` | instrukcja warunkowa |
| 🔁 | `WHILE` | pętla while |
| 📂 / 📁 | `LBRACKET` / `RBRACKET` | lista `[` / `]` |
| 🎯 / 📏 / 🖇️ | `AT` / `LEN` / `APPEND` | indeks / długość / dopisz |
| 🎁 / 📞 / 🔙 | `FUNC` / `CALL` / `RETURN` | definicja / wywołanie / zwróć |
| `#…` | — | komentarz (pomijany) |
| spacja, tab, `\r` | — | pomijane |

Uwaga: tokeny `✖️`, `⚖️`, `🖇️` mają w skanerze opcjonalny selektor
wariantu U+FE0F (kwantyfikator `?`), aby rozpoznać obie postacie symbolu.

---

## 5. Gramatyka formatu

Notacja generatora Yacc/PLY, bez akcji semantycznych. Gramatyka jest
**poprawnie rozbita na poziomy**:

- jednorodny poziom instrukcji: jeden `statement`, jeden wspólny `block`
  (dla `if`/`while`/`for`/funkcji);
- **warstwowy poziom wyrażeń**: każdy priorytet operatora to osobny
  nieterminał (`or_expr` → `and_expr` → `not_expr` → `comparison` →
  `additive` → `multiplicative` → `unary` → `postfix` → `primary`).

Dzięki temu priorytety i łączność wynikają **ze struktury gramatyki**, a nie
z dyrektyw — gramatyka jest jednoznaczna i wolna od konfliktów *shift/reduce*
bez użycia tabeli `precedence`.

```yacc
%token ID NUMBER STRING TRUE FALSE
%token ASSIGN END EXIT
%token LBRACE RBRACE LPAREN RPAREN COMMA
%token PRINT INPUT
%token PLUS MINUS TIMES DIVIDE
%token EQ NEQ LT GT LE GE
%token AND OR NOT
%token NUM_CAST
%token IF ELSE WHILE
%token LBRACKET RBRACKET AT LEN APPEND
%token FUNC CALL RETURN

%%

program     : statements ;

statements  : statements statement
            | statement ;

statement   : assignment   END
            | print_stmt    END
            | append_stmt   END
            | expression    END
            | return_stmt   END    /* poprawne tylko w funkcji (kontrola semantyczna) */
            | EXIT          END
            | if_stmt
            | while_stmt
            | func_def ;

block       : LBRACE statements RBRACE
            | LBRACE RBRACE ;

assignment  : ID ASSIGN expression ;
print_stmt  : PRINT arglist ;
append_stmt : ID APPEND expression ;

if_stmt     : IF expression block
            | IF expression block ELSE block ;
while_stmt  : WHILE expression block ;

func_def    : FUNC ID LPAREN params RPAREN block
            | FUNC ID LPAREN RPAREN block ;
params      : params COMMA ID
            | ID ;
return_stmt : RETURN expression ;

/* --- wyrażenia: hierarchia poziomów priorytetu (od najsłabszego) --- */
expression     : or_expr ;
or_expr        : or_expr OR and_expr
               | and_expr ;
and_expr       : and_expr AND not_expr
               | not_expr ;
not_expr       : NOT not_expr
               | comparison ;
comparison     : comparison EQ  additive
               | comparison NEQ additive
               | comparison LT  additive
               | comparison GT  additive
               | comparison LE  additive
               | comparison GE  additive
               | additive ;
additive       : additive PLUS  multiplicative
               | additive MINUS multiplicative
               | multiplicative ;
multiplicative : multiplicative TIMES  unary
               | multiplicative DIVIDE unary
               | unary ;
unary          : MINUS unary
               | LEN   unary
               | postfix ;
postfix        : postfix AT primary
               | primary ;
primary        : NUM_CAST LPAREN expression RPAREN
               | LBRACKET arglist RBRACKET
               | LBRACKET RBRACKET
               | CALL ID LPAREN arglist RPAREN
               | CALL ID LPAREN RPAREN
               | INPUT
               | LPAREN expression RPAREN
               | NUMBER | STRING | TRUE | FALSE | ID ;

arglist     : arglist COMMA expression
            | expression ;
```

Uwagi:

- Lewa rekurencja na poziomach binarnych (`additive : additive PLUS multiplicative`)
  daje **łączność lewostronną**: `a − b − c = (a − b) − c`.
- Operatory przedrostkowe (`🚫`, `📏`, unarny `➖`) tworzą poziom `unary`;
  indeksowanie `🎯` to poziom `postfix` (wiąże najmocniej). Każdy poziom
  odwołuje się tylko do poziomu wiążącego mocniej.
- Instrukcje proste kończy `🔚`; instrukcje złożone (`if`/`while`/funkcja)
  kończy ich blok `🛑`.
- `return_stmt` to składniowo zwykła instrukcja prosta (jak w Pythonie),
  zgrupowana przy funkcjach. Użycie `🔙` poza funkcją wykrywane jest na etapie wykonania.
- Blok domyka każdą gałąź `if`/`else`, więc problem „wiszącego else" nie występuje.

---

## 6. Generatory i pakiety zewnętrzne

| Pakiet | Rola |
| --- | --- |
| PLY (`ply.lex`, `ply.yacc`) | generatory skanera i parsera LALR(1) |
| Flask | serwer interfejsu webowego (Web UI) |

Instalacja: `pip install ply flask`.

---

## 7. Krótka instrukcja obsługi

Tryb webowy (z klikalną paletą emoji):

```bash
python web_ui.py        # następnie: http://127.0.0.1:5000
```

Tryb konsolowy:

```bash
python main.py demo.emo
python main.py demo.emo < dane.txt
```

---

## 8. Przykład użycia

```
🎁 silnia ( n ) 🧱
    ❓ n 🔽 1 🧱
        🔙 1 🔚
    🛑
    🔙 n ✖️ 📞 silnia ( n ➖ 1 ) 🔚
🛑

wynik 📦 📞 silnia ( 5 ) 🔚
📢 💬Silnia z 5 to:💬 📍 wynik 🔚
🏁 🔚
```

Wynik: `Silnia z 5 to: 120`

Pozostałe przykłady: `demo.emo` (pętla, lista, warunek, wejście),
`lista.emo` (operacje na listach).

---

## 9. Inne informacje

Struktura projektu:

| Plik | Zawartość |
| --- | --- |
| `lexer.py` | skaner PLY (definicje tokenów — jedyne miejsce z emoji) |
| `parser_yacc.py` | gramatyka PLY (LALR) + budowa AST |
| `ast_nodes.py` | węzły AST z metodami `eval`, środowisko zmiennych, błędy |
| `interpreter.py` | rdzeń: parsowanie + uruchamianie z przechwyceniem I/O |
| `main.py` | interfejs konsolowy |
| `web_ui.py` | interfejs webowy (Flask) z paletą emoji |
| `*.emo` | przykładowe programy |

Wykonanie: każdy węzeł AST ma metodę `eval(env)`. Wywołanie funkcji tworzy
lokalne środowisko z rodzicem globalnym (funkcja widzi globalne i własne
parametry; rekurencja działa). Wymagane pakiety: `ply`, `flask`.
