# Przedmiot: Teoria kompilacji i kompilatory

# EmoLang – Interpreter języka emotikonowego

**Przedmiot:** Teoria kompilacji i kompilatory  
**Autorzy:** Bednarski Paweł, Czosnek Bartłomiej  

---

## Opis projektu

**EmoLang** to interpreter języka dziedzinowego (DSL) zaprojektowanego w celu eksploracji koncepcji egzotycznych języków programowania (esolangs). Unikalną cechą systemu jest zastąpienie klasycznych słów kluczowych i operatorów znakami Unicode z zestawu **Emoji**. Język pozwala na pełną kontrolę nad przepływem sterowania, operacje na zmiennych oraz proste obliczenia matematyczne w sposób czytelny i angażujący.

System analizuje kod źródłowy zapisany w plikach `.emo`, buduje drzewo składniowe (AST) i wykonuje instrukcje w środowisku Python. Architektura projektu skupia się na rygorystycznym oddzieleniu fazy analizy leksykalnej i składniowej od fazy wykonawczej (interpretera), co zapewnia łatwą rozszerzalność o nowe symbole i funkcjonalności.

## Wymagania

### Funkcjonalne
* **Parser i interpreter języka EmoLang** – pełna obsługa cyklu odczytu i wykonania kodu.
* **Zmienne i typy danych** – wsparcie dla dynamicznego typowania (liczby całkowite, napisy).
* **Operacje arytmetyczne** – implementacja podstawowej matematyki za pomocą emoji (np. ➕, ➖, ✖️, ➗).
* **Struktury sterujące** – obsługa logiki warunkowej (❓) oraz zapętlania instrukcji (🔁).
* **Instrukcje I/O** – interakcja z użytkownikiem poprzez konsolę (wypisywanie 📢).
* **Obsługa błędów** – wykrywanie błędów składniowych oraz wyjątków czasu wykonania (np. brak zdefiniowanej zmiennej).

### Niefunkcjonalne
* **Python 3.10+** – silnik wykonawczy interpretera.
* **Zgodność z UTF-8** – natywne wsparcie dla szerokiej gamy symboli Unicode.
* **Modularna architektura** – podział na lekser, parser, AST oraz wizytator/interpreter.
* **Czytelny DSL** – intuicyjne mapowanie wizualne symboli na ich funkcje logiczne.

## Parser / Skaner

Analiza składniowa oraz skanowanie tokenów realizowane są przy użyciu biblioteki **PLY (Python Lex-Yacc)** (lub opcjonalnie **Lark**). Narzędzia te pozwalają na generowanie efektywnego parsera LALR na podstawie formalnie zdefiniowanej gramatyki bezkontekstowej.
