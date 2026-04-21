# TODO – EmoLang Interpreter

## 📁 Struktura projektu

### 🔧 Pliki źródłowe interpretera

* [ ] **emoti_interpreter.py** (Punkt wejścia)

  * [ ] Obsługa argumentów CLI (`sys.argv`)
  * [ ] Odczyt pliku `.emo` (UTF-8)
  * [ ] Przekazanie kodu do:

    * [ ] lexera
    * [ ] parsera
    * [ ] interpretera

* [ ] **lexer.py** (Analizator leksykalny – PLY)

  * [ ] Zdefiniowanie listy `tokens`
  * [ ] Reguły dla emotikon:

    * [ ] 📢 → PRINT
    * [ ] 💬...💬 → STRING
    * [ ] 📥 → INPUT
    * [ ] inne operatory/emotikony
  * [ ] Obsługa liczb, identyfikatorów
  * [ ] Ignorowanie:

    * [ ] spacji
    * [ ] nowych linii (jeśli trzeba)
    * [ ] komentarzy

* [ ] **parser.py** (Analizator składniowy – PLY)

  * [ ] Implementacja gramatyki
  * [ ] Funkcje `p_*` dla reguł:

    * [ ] przypisania
    * [ ] wyrażeń
    * [ ] print
    * [ ] input
    * [ ] warunków (if)
    * [ ] pętli (jeśli są)
  * [ ] Budowanie AST (z użyciem `ast_nodes.py`)

* [ ] **ast_nodes.py** (Drzewo AST)

  * [ ] Klasy węzłów:

    * [ ] `PrintNode`
    * [ ] `InputNode`
    * [ ] `BinaryOpNode`
    * [ ] `NumberNode`
    * [ ] `StringNode`
    * [ ] `VariableNode`
    * [ ] `AssignmentNode`
    * [ ] `IfNode`
    * [ ] (opcjonalnie) `WhileNode`, `ListNode`
  * [ ] Przechowywanie danych węzłów

* [ ] **interpreter.py** (Ewaluator / Visitor)

  * [ ] Implementacja wykonywania AST
  * [ ] Obsługa:

    * [ ] print → `print()`
    * [ ] input → `input()`
    * [ ] operacji matematycznych
    * [ ] warunków
  * [ ] Visitor pattern (np. `visit_*`)

* [ ] **environment.py** (Stan programu)

  * [ ] Słownik zmiennych (`dict`)
  * [ ] Metody:

    * [ ] get
    * [ ] set
  * [ ] Obsługa typów:

    * [ ] liczby
    * [ ] stringi
    * [ ] listy

---

## 📦 Pliki konfiguracyjne

* [ ] **requirements.txt**

  * [ ] `ply==3.11` (lub nowsze)

* [ ] **README.md**

  * [ ] Opis języka EmoLang
  * [ ] Instrukcja uruchomienia
  * [ ] Przykłady

---

## 🧪 Pliki testowe

* [ ] **demo.emo**

  * [ ] Prosty test:

    * [ ] print
    * [ ] input
    * [ ] operacje

* [ ] **examples/**

  * [ ] `loops.emo` – pętle
  * [ ] `conditions.emo` – warunki
  * [ ] `lists.emo` – listy
  * [ ] `casting.emo` – rzutowanie

---

## 🚀 Dodatkowe zadania

* [ ] Obsługa błędów:

  * [ ] leksykalnych
  * [ ] składniowych
  * [ ] wykonania

* [ ] Debugowanie:

  * [ ] podgląd tokenów
  * [ ] podgląd AST

* [ ] Rozszerzenia języka:

  * [ ] nowe emotikony
  * [ ] funkcje
  * [ ] typy danych

---

## ✅ Pipeline interpretera

1. Odczyt pliku `.emo`
2. Tokenizacja (lexer)
3. Parsowanie → AST
4. Interpretacja (execution)

---

## 🎯 Cel

Stworzyć działający interpreter języka EmoLang z czytelną architekturą:
**Wejście → Tokeny → AST → Wykonanie**
