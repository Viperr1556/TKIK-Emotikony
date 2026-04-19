### Tabela Tokenów: EmoLang ➡️ Specyfikacja Leksera

| Kategoria | Symbol / Format | Token (PLY) | Opis / Działanie |
| :--- | :---: | :--- | :--- |
| **Zmienne** | `[a-z_][a-z0-9_]*` | `ID` | Nazwa zmiennej (identyfikator) |
| **Liczby** | `[0-9]+(\.[0-9]+)?` | `NUMBER` | Literał liczbowy (int/float) |
| **Tekst** | Zawartość między 💬 | `STRING` | Literał tekstowy (String) |
| **Typy i Wartości** | 📦 | `ASSIGN` | Operator przypisania |
| | ✅ | `TRUE` | Wartość logiczna: Prawda |
| | ❌ | `FALSE` | Wartość logiczna: Fałsz |
| | 💬 | `QUOTE` | Ogranicznik tekstu |
| | 🔢 | `INT_CAST` | Konwersja na liczbę całkowitą |
| | 📉 | `FLOAT_CAST` | Konwersja na liczbę zmiennoprzecinkową |
| | 🔤 | `STR_CAST` | Konwersja na typ tekstowy |
| **Listy (Tablice)** | 📂 | `LBRACKET` | Otwarcie listy |
| | 📁 | `RBRACKET` | Zamknięcie listy |
| | 🎯 | `AT` | Dostęp do indeksu (indeksowanie) |
| | 📏 | `LEN` | Pobranie długości (listy lub tekstu) |
| | 🖇️ | `APPEND` | Metoda dopisywania do listy |
| **Wejście / Wyjście**| 📢 | `PRINT` | Wypisanie na standardowe wyjście |
| | 📥 | `INPUT` | Pobranie danych od użytkownika |
| | 📍 | `COMMA` | Separator argumentów |
| **Arytmetyka** | ➕ | `PLUS` | Dodawanie |
| | ➖ | `MINUS` | Odejmowanie |
| | ✖️ | `MULTIPLY` | Mnożenie |
| | ➗ | `DIVIDE` | Dzielenie |
| **Logika** | 🔀 | `OR` | Alternatywa logiczna |
| | 🔗 | `AND` | Koniunkcja logiczna |
| | 🚫 | `NOT` | Negacja logiczna |
| **Porównania** | ⚖️ | `EQ` | Równe |
| | 💔 | `NEQ` | Różne |
| | 👈 | `LT` | Mniejsze niż |
| | 👉 | `GT` | Większe niż |
| | 👈⚖️ | `LE` | Mniejsze lub równe |
| | 👉⚖️ | `GE` | Większe lub równe |
| **Sterowanie** | ❓ | `IF` | Instrukcja warunkowa |
| | 💡 | `ELSE` | Blok "w przeciwnym razie" |
| | 🔁 | `WHILE` | Pętla (dopóki) |
| | 🧱 | `LBRACE` | Rozpoczęcie bloku kodu |
| | 🛑 | `RBRACE` | Zakończenie bloku kodu |
| | 🔚 | `NEWLINE` | Koniec instrukcji (nowa linia) |
| | 🏁 | `EXIT` | Zakończenie pracy interpretera |
| **Techniczne** | `(` | `LPAREN` | Nawias otwierający |
| | `)` | `RPAREN` | Nawias zamykający |
| | `#` | `COMMENT` | Komentarz (ignorowany przez lekser) |
