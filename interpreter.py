# -*- coding: utf-8 -*-
"""
EmoLang - wspólny rdzeń uruchomieniowy.

Tu spina się wszystko w całość:
    tekst programu  --(lexer)-->  tokeny  --(parser)-->  AST  --(eval)-->  wynik

Funkcji `run_capture` używa interfejs webowy: przechwytuje to, co program
wypisuje (stdout) i podaje mu wcześniej przygotowane dane wejściowe (stdin).
Tryb konsolowy (main.py) uruchamia AST bezpośrednio - interaktywnie.
"""

import io
import sys

from lexer import lexer
from parser_yacc import parser
from ast_nodes import Environment, EmoError, ReturnSignal


def parse_program(code):
    """Zamienia tekst na AST (albo None, gdy program jest pusty/błędny)."""
    lexer.lineno = 1
    return parser.parse(code, lexer=lexer)


def run_capture(code, stdin_text=""):
    """Uruchamia program i zwraca jego wyjście jako tekst.

    `stdin_text` to dane, które program odczyta przez 📥 (każda linia = jedno
    wczytanie). Używane przez interfejs webowy."""
    output = io.StringIO()
    old_stdout, old_stdin = sys.stdout, sys.stdin
    sys.stdout = output
    sys.stdin = io.StringIO(stdin_text)
    try:
        ast = parse_program(code)
        if ast is not None:
            ast.eval(Environment())
    except ReturnSignal:
        print("🔥 Błąd wykonania: 🔙 (zwróć) użyto poza funkcją")
    except EmoError as e:
        print(f"🔥 Błąd wykonania: {e}")
    except RecursionError:
        print("🔥 Błąd wykonania: zbyt głęboka rekurencja")
    except Exception as e:
        print(f"🔥 Błąd krytyczny: {e}")
    finally:
        sys.stdout, sys.stdin = old_stdout, old_stdin
    return output.getvalue()
