import sys
from interpreter import parse_program
from compiler import compile_ast
from vm import VM
from ast_nodes import Environment, EmoError, ReturnSignal


def main():
    if len(sys.argv) < 2:
        print("Użycie: python main.py program.emo")
        return
    try:
        code = open(sys.argv[1], encoding="utf-8").read()
    except OSError as e:
        print(f"Nie można otworzyć pliku: {e}"); return

    ast = parse_program(code)
    if ast is None: return
    try:
        VM().run(compile_ast(ast), Environment())
    except ReturnSignal:
        print("🔥 Błąd wykonania: 🔙 (zwróć) użyto poza funkcją")
    except EmoError as e:
        print(f"🔥 Błąd wykonania: {e}")


if __name__ == "__main__":
    main()
