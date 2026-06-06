# -*- coding: utf-8 -*-
"""
EmoLang - tryb konsolowy.

Użycie:
    python main.py program.emo

Program jest wykonywany interaktywnie: 📢 pisze wprost na ekran, a 📥 czyta
z klawiatury. (Interfejs webowy uruchamiamy osobno: python web_ui.py)
"""

import sys

from interpreter import parse_program
from ast_nodes import Environment, EmoError, ReturnSignal


def main():
    if len(sys.argv) < 2:
        print("Użycie: python main.py program.emo")
        return

    path = sys.argv[1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()
    except OSError as e:
        print(f"Nie można otworzyć pliku: {e}")
        return

    ast = parse_program(code)
    if ast is None:
        return
    try:
        ast.eval(Environment())
    except ReturnSignal:
        print("🔥 Błąd wykonania: 🔙 (zwróć) użyto poza funkcją")
    except EmoError as e:
        print(f"🔥 Błąd wykonania: {e}")


if __name__ == "__main__":
    main()
