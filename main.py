import sys
import io
import html
from contextlib import redirect_stdout

from parser_yacc import parser
from ast_nodes import Environment


OUTPUT_HTML = "output.html"
OUTPUT_TXT = "output.txt"


def save_output(filename, result):
    escaped = html.escape(result)

    with open(OUTPUT_TXT, "w", encoding="utf-8") as f:
        f.write(result)

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="1">
    <title>EmoLang Output</title>
    <style>
        body {{
            font-family: Consolas, monospace;
            background: #1e1e1e;
            color: #f5f5f5;
            padding: 30px;
        }}
        pre {{
            background: #2b2b2b;
            padding: 20px;
            border-radius: 10px;
            white-space: pre-wrap;
        }}
    </style>
</head>
<body>
    <h1>Wynik interpretera EmoLang</h1>
    <p>Plik: <b>{html.escape(filename)}</b></p>
    <pre>{escaped}</pre>
</body>
</html>
""")


def run_interpreter(filename):
    buffer = io.StringIO()

    try:
        with open(filename, "r", encoding="utf-8") as f:
            code = f.read()

        with redirect_stdout(buffer):
            ast = parser.parse(code)
            if ast:
                global_env = Environment()
                ast.eval(global_env)

    except Exception as e:
        buffer.write(f"Krytyczny błąd: {e}\n")

    result = buffer.getvalue()
    print(result, end="")
    save_output(filename, result)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_interpreter(sys.argv[1])
    else:
        print("Użycie: python main.py plik.emo")
