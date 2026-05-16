import os
import io
from contextlib import redirect_stdout
from unittest.mock import patch

from flask import Flask, request, render_template_string

from parser_yacc import parser
from ast_nodes import Environment


app = Flask(__name__)

# Szuka plików .emo w tym samym folderze co web_ui.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


HTML = """
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <title>EmoLang Web UI</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #1e1e1e;
            color: #f5f5f5;
            padding: 30px;
        }

        h1 {
            margin-bottom: 20px;
        }

        form {
            background: #2b2b2b;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
        }

        select, button, textarea {
            font-size: 16px;
            padding: 10px;
            border-radius: 8px;
            border: none;
            margin-top: 10px;
        }

        select {
            min-width: 280px;
        }

        textarea {
            width: 100%;
            min-height: 100px;
            box-sizing: border-box;
            font-family: Consolas, monospace;
            resize: vertical;
        }

        button {
            cursor: pointer;
            background: #4caf50;
            color: white;
            margin-top: 15px;
        }

        pre {
            background: #2b2b2b;
            padding: 20px;
            border-radius: 12px;
            white-space: pre-wrap;
            font-family: Consolas, monospace;
        }

        .label {
            margin-top: 15px;
            display: block;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>EmoLang Interpreter</h1>

    <form method="POST">
        <label class="label">Wybierz plik .emo:</label>

        <select name="filename">
            {% for file in files %}
                <option value="{{ file }}" {% if file == selected %}selected{% endif %}>
                    {{ file }}
                </option>
            {% endfor %}
        </select>

        <label class="label">Dane wejściowe dla input(), każda wartość w osobnej linii:</label>

        <textarea name="user_input" placeholder="Np. dla 03_if_else.emo wpisz tutaj liczbę">{{ user_input }}</textarea>

        <br>

        <button type="submit">Uruchom program</button>
    </form>

    {% if selected %}
        <h2>Wynik dla: {{ selected }}</h2>
    {% else %}
        <h2>Wynik</h2>
    {% endif %}

    <pre>{{ output }}</pre>
</body>
</html>
"""


def run_emo_file(filepath, user_input=""):
    buffer = io.StringIO()

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()

        input_lines = iter(user_input.splitlines())

        def fake_input():
            return next(input_lines, "")

        with redirect_stdout(buffer), patch("builtins.input", fake_input):
            ast = parser.parse(code)

            if ast:
                global_env = Environment()
                ast.eval(global_env)

    except Exception as e:
        buffer.write(f"Błąd: {e}")

    return buffer.getvalue()


@app.route("/", methods=["GET", "POST"])
def index():
    files = sorted([
        f for f in os.listdir(BASE_DIR)
        if f.endswith(".emo")
    ])

    output = ""
    selected = None
    user_input = ""

    if request.method == "POST":
        selected = request.form.get("filename")
        user_input = request.form.get("user_input", "")

        filepath = os.path.join(BASE_DIR, selected)

        if selected not in files:
            output = "Błąd: wybrano nieprawidłowy plik."
        else:
            output = run_emo_file(filepath, user_input)

    return render_template_string(
        HTML,
        files=files,
        output=output,
        selected=selected,
        user_input=user_input
    )


if __name__ == "__main__":
    app.run(debug=True)
