# 🗺️ Harmonogram i postęp prac (Roadmap) - EmoLang

Wykaz zrealizowanych i planowanych etapów projektu z przedmiotu *Teoria kompilacji i kompilatory*.

## Faza 1: Wstępna (Zakończona ✅)
- [x] **Wybór tematu projektu:** EmoLang (Interpreter języka opartego na emoji).
- [x] Uzgodnienie tematu z prowadzącym.
- [x] Dopisanie tematu do listy projektów.
- [x] Wstępne uzupełnienie dokumentacji na GitHubie (punkty 1-3).

## Faza 2: Specyfikacja i Prototyp (Zakończona ✅)
- [x] **Spis tokenów i gramatyka:** - [x] Implementacja pełnego spisu tokenów z uwzględnieniem znaków wielobajtowych (Unicode).
  - [x] Opracowanie gramatyki bezkontekstowej (rozwiązanie konfliktów Shift/Reduce, ustalenie priorytetów operatorów).
  - [x] Dopisanie specyfikacji do dokumentacji.
- [x] Prezentacja stanu prac.
- [x] **Prototyp:**
  - [x] Stworzenie i zintegrowanie Lexera, Parsera (Yacc) i drzewa AST.
  - [x] Wstępna wersja dokumentacji (README.md).
  - [x] Prezentacja działającej aplikacji (odczyt kodu z pliku `.emo`, poprawne ewaluowanie instrukcji m.in. rekurencji i pętli).

---

## Faza 3: Wersja ℬ-wersja (W trakcie ⏳)
*Cel: Dopracowanie prototypu do "prawie końcowej" wersji aplikacji (tzw. Feature Freeze).*
- [ ] **Techniczne usprawnienia interpretera:**
  - [ ] Wzmocnienie obsługi błędów (np. ładniejsze komunikaty o dzieleniu przez zero, precyzyjne wskazywanie numeru linii w AST).
  - [ ] Rozbudowa operacji na stringach (np. łączenie tekstów za pomocą operatora `➕`).
  - [ ] Stworzenie dodatkowych skryptów testowych `.emo` (np. sortowanie bąbelkowe, ciąg Fibonacciego), aby udowodnić stabilność języka.
- [ ] Aktualizacja obecnej wersji dokumentacji o ewentualne nowe tokeny/złożoności wypracowane podczas testów.
- [ ] **Prezentacja ℬ-wersji** przed prowadzącym.

## Faza 4: Zaliczenie i Wersja Końcowa (Planowane 🔴)
*Cel: Ostateczny szlif projektu, wyeliminowanie ostatnich bugów i oddanie całości.*
- [ ] Pełne testy regresyjne całego interpretera.
- [ ] Przegląd i formatowanie kodu źródłowego (refaktoryzacja).
- [ ] Sporządzenie **pełnego sprawozdania** / końcowej wersji dokumentacji (wypolerowanie pliku README.md do ostatecznej formy).
- [ ] Oddanie projektu (wypchnięcie ostatecznego commitu na branch główny).
- [ ] **Prezentacja aplikacji (Zaliczenie).**
