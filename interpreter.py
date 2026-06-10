import io, sys

from lexer import lexer
from parser_yacc import parser
from compiler import compile_ast, disassemble
from vm import VM
from ast_nodes import Environment, EmoError, ReturnSignal


def parse_program(code):
    lexer.lineno = 1
    return parser.parse(code, lexer=lexer)


def run_capture(code, stdin_text="", show_bytecode=False):
    """Uruchamia program i zwraca wyjście jako tekst."""
    output = io.StringIO()
    old_stdout, old_stdin = sys.stdout, sys.stdin
    sys.stdout = output
    sys.stdin = io.StringIO(stdin_text)
    try:
        ast = parse_program(code)
        if ast is not None:
            bytecode = compile_ast(ast)
            if show_bytecode:
                print("--- bajtkod ---")
                print(disassemble(bytecode))
                print("--- wynik ---")
            VM().run(bytecode, Environment())
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
