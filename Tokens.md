### Tabela Tokenów: EmoLang ➡️ Python

Poniższa tabela zawiera kompletny zestaw symboli emotikonowych wykorzystywanych przez lekser EmoLang oraz ich bezpośrednie mapowanie na składnię lub zachowanie w języku Python.

| Kategoria | Emotikon | Token Python | Opis / Działanie |
| :--- | :---: | :--- | :--- |
| **Typy i Wartości** | 📦 | `=` | Przypisanie (inicjalizacja zmiennej) |
| | ✅ | `True` | Wartość logiczna: Prawda |
| | ❌ | `False` | Wartość logiczna: Fałsz |
| | 💬 | `"` | Cudzysłów (rozpoczęcie/zakończenie tekstu) |
| | 🔢 | `int()` | Rzutowanie na liczbę całkowitą |
| | 📉 | `float()` | Rzutowanie na liczbę zmiennoprzecinkową |
| | 🔤 | `str()` | Rzutowanie na typ tekstowy |
| **Wejście / Wyjście**| 📢 | `print()` | Wypisanie danych na standardowe wyjście |
| | 📍 | `,` | Separator argumentów (np. przy wypisywaniu) |
| **Arytmetyka** | ➕ | `+` | Operator dodawania |
| | ➖ | `-` | Operator odejmowania |
| | ✖️ | `*` | Operator mnożenia |
| | ➗ | `/` | Operator dzielenia |
| **Logika** | 🔀 | `or` | Alternatywa logiczna (LUB) |
| | 🔗 | `and` | Koniunkcja logiczna (I) |
| | 🚫 | `not` | Negacja logiczna (NIE) |
| **Porównania** | ⚖️ | `==` | Równe |
| | 💔 | `!=` | Różne |
| | 👈 | `<` | Mniejsze niż |
| | 👉 | `>` | Większe niż |
| | 👈⚖️ | `<=` | Mniejsze lub równe |
| | 👉⚖️ | `>=` | Większe lub równe |
| **Struktura** | ❓ | `if` | Instrukcja warunkowa |
| | 🔁 | `while` | Pętla (dopóki) |
| | 🧱 | `:` | Rozpoczęcie bloku kodu (wymusza wcięcie poziomu niżej) |
| | 🛑 | `end` | Zakończenie bloku kodu (powrót do wyższego wcięcia) |
| | 🔚 | `\n` | Znak nowej linii / koniec bieżącej instrukcji |
| | 🏁 | `exit()` | Zakończenie działania programu |

| Element | Format / Znak | Opis i Zasady |
| :--- | :--- | :--- |
| **Zmienne (Identyfikatory)** | `[a-zA-Z_][a-zA-Z0-9_]*` | Nazwy zmiennych używają standardowych liter alfabetu, cyfr i znaku podkreślenia. Nie mogą zaczynać się od cyfry. (np. `licznik`, `moja_wartosc_2`). |
| **Liczby surowe** | `[0-9]+` lub `[0-9]+\.[0-9]+` | Cyfry arabskie wpisywane bezpośrednio (np. `42`, `3.14`). Można je łączyć z 🔢 i 📉 w celu rzutowania typów. |
| **Zawartość Stringów** | Zwykły tekst | Dowolne znaki i słowa wpisywane pomiędzy emotikonami cudzysłowu. (np. `💬 Witaj świecie! 💬`). |
| **Nawiasy grupujące** | `(` oraz `)` | Standardowe nawiasy okrągłe do wymuszania kolejności wykonywania działań matematycznych lub logicznych. (np. `( 2 ➕ 2 ) ✖️ 2`). |
| **Wcięcia (Indentation)** | Spacje lub Tabulatory | Białe znaki na początku linii. Po otwarciu bloku kodu emotikonem `🧱`, każda linia należąca do tego bloku musi być poprzedzona wcięciem (np. 4 spacje). |
| **Komentarze** | `#` | Standardowy znak krzyżyka (hash). Wszystko od tego znaku do końca linii jest ignorowane przez interpreter. |
