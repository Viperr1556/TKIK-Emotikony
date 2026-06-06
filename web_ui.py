# -*- coding: utf-8 -*-
"""
EmoLang - interfejs webowy (Flask).

Uruchomienie:
    python web_ui.py
a następnie w przeglądarce:  http://127.0.0.1:5000

Pozwala pisać kod .emo bez kopiowania emoji (klikalna paleta), podać dane
wejściowe i zobaczyć wynik. Pod spodem używa tego samego interpretera co
tryb konsolowy (interpreter.run_capture) - nic nie jest tłumaczone na Pythona.
"""

from flask import Flask, request, jsonify, render_template_string
from interpreter import run_capture

app = Flask(__name__)

# Paleta: grupy (nazwa, [(emoji, podpis/znaczenie), ...])
PALETTE = [
    ("Wartości / zmienne", [
        ("📦", "przypisz (x 📦 5)"), ("🔚", "koniec instrukcji"),
        ("💬", "tekst 💬…💬"), ("✅", "prawda"), ("❌", "fałsz"),
    ]),
    ("Arytmetyka", [
        ("➕", "dodaj"), ("➖", "odejmij"), ("✖️", "pomnóż"), ("➗", "podziel"),
    ]),
    ("Porównania", [
        ("⚖️", "równe =="), ("💔", "różne !="), ("👈", "mniejsze <"),
        ("👉", "większe >"), ("🔽", "mniejsze-równe <="), ("🔼", "większe-równe >="),
    ]),
    ("Logika", [
        ("🔗", "i (and)"), ("🔀", "lub (or)"), ("🚫", "nie (not)"),
    ]),
    ("Sterowanie", [
        ("❓", "jeżeli"), ("💡", "w przeciwnym razie"), ("🔁", "dopóki (while)"),
        ("🧱", "początek bloku {"), ("🛑", "koniec bloku }"),
    ]),
    ("Wejście / wyjście", [
        ("📢", "wypisz"), ("📥", "wczytaj linię"), ("🔢", "na liczbę"),
    ]),
    ("Listy", [
        ("📂", "początek listy ["), ("📁", "koniec listy ]"),
        ("🎯", "element pod indeksem"), ("📏", "długość"), ("🖇️", "dopnij element"),
    ]),
    ("Funkcje", [
        ("🎁", "definicja funkcji"), ("📞", "wywołanie funkcji"),
        ("🔙", "zwróć wartość"), ("📍", "przecinek (separator)"),
        ("(", "nawias ("), (")", "nawias )"),
    ]),
    ("Inne", [
        ("🏁", "koniec programu"),
    ]),
]

EXAMPLES = {
    "silnia": (
        "🎁 silnia ( n ) 🧱\n"
        "    ❓ n 🔽 1 🧱\n"
        "        🔙 1 🔚\n"
        "    🛑\n"
        "    🔙 n ✖️ 📞 silnia ( n ➖ 1 ) 🔚\n"
        "🛑\n\n"
        "wynik 📦 📞 silnia ( 5 ) 🔚\n"
        "📢 💬Silnia z 5 to:💬 📍 wynik 🔚\n"
        "🏁 🔚\n"
    ),
    "lista": (
        "owoce 📦 📂 💬jablko💬 📍 💬gruszka💬 📁 🔚\n"
        "owoce 🖇️ 💬sliwka💬 🔚\n"
        "📢 💬Lista:💬 📍 owoce 🔚\n"
        "📢 💬Dlugosc:💬 📍 📏 owoce 🔚\n"
        "📢 💬Pierwszy:💬 📍 owoce 🎯 0 🔚\n"
        "🏁 🔚\n"
    ),
    "wejscie": (
        "📢 💬Podaj swoje imie:💬 🔚\n"
        "imie 📦 📥 🔚\n"
        "📢 💬Witaj,💬 📍 imie 🔚\n"
        "📢 💬Podaj liczbe:💬 🔚\n"
        "x 📦 🔢 ( 📥 ) 🔚\n"
        "📢 💬Kwadrat:💬 📍 x ✖️ x 🔚\n"
        "🏁 🔚\n"
    ),
}

PAGE = r"""<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>EmoLang IDE</title>
<style>
  :root{
    --bg:#14110f; --panel:#1d1916; --panel2:#262019; --ink:#f3ead9;
    --muted:#9b8f7d; --accent:#e8a33d; --accent2:#c2410c; --line:#3a3128;
    --ok:#7bbf6a; --mono:"JetBrains Mono","DejaVu Sans Mono",ui-monospace,monospace;
    --disp:"Iowan Old Style","Palatino Linotype",Georgia,serif;
  }
  *{box-sizing:border-box}
  body{
    margin:0; background:
      radial-gradient(900px 500px at 85% -10%, rgba(232,163,61,.10), transparent 60%),
      repeating-linear-gradient(0deg, transparent 0 38px, rgba(255,255,255,.012) 38px 39px),
      var(--bg);
    color:var(--ink); font-family:var(--mono); line-height:1.5;
  }
  header{padding:26px 32px 14px; border-bottom:1px solid var(--line)}
  h1{font-family:var(--disp); font-weight:600; font-size:30px; margin:0; letter-spacing:.3px}
  h1 .dot{color:var(--accent)}
  header p{margin:4px 0 0; color:var(--muted); font-size:13px}
  .wrap{display:grid; grid-template-columns: 300px 1fr; gap:0; min-height:calc(100vh - 92px)}
  /* paleta */
  aside{border-right:1px solid var(--line); padding:18px; overflow:auto; max-height:calc(100vh - 92px)}
  .grp{margin-bottom:16px}
  .grp h3{font-size:11px; text-transform:uppercase; letter-spacing:1.5px; color:var(--muted);
    margin:0 0 8px; font-family:var(--mono)}
  .keys{display:flex; flex-wrap:wrap; gap:6px}
  .key{position:relative; background:var(--panel2); border:1px solid var(--line);
    border-radius:9px; padding:7px 9px; font-size:18px; cursor:pointer; line-height:1;
    transition:transform .08s ease, border-color .15s ease, background .15s ease}
  .key:hover{transform:translateY(-2px); border-color:var(--accent); background:#2f2619}
  .key:active{transform:translateY(0)}
  .key .tip{position:absolute; bottom:115%; left:50%; transform:translateX(-50%);
    background:#000; color:var(--ink); font-size:11px; padding:4px 8px; border-radius:6px;
    white-space:nowrap; opacity:0; pointer-events:none; transition:opacity .12s; z-index:5;
    border:1px solid var(--line)}
  .key:hover .tip{opacity:1}
  /* główny obszar */
  main{padding:18px 22px; display:flex; flex-direction:column; gap:14px}
  .row{display:flex; align-items:center; justify-content:space-between; gap:12px}
  label{font-size:11px; text-transform:uppercase; letter-spacing:1.5px; color:var(--muted)}
  textarea{width:100%; background:var(--panel); color:var(--ink); border:1px solid var(--line);
    border-radius:12px; padding:14px; font-family:var(--mono); font-size:16px; resize:vertical;
    outline:none}
  textarea:focus{border-color:var(--accent)}
  #code{min-height:300px; flex:1}
  #stdin{min-height:64px}
  .bar{display:flex; gap:10px; align-items:center; flex-wrap:wrap}
  button.run{background:linear-gradient(180deg,var(--accent),var(--accent2)); color:#1a1206;
    border:none; padding:11px 22px; border-radius:10px; font-family:var(--mono); font-weight:700;
    font-size:14px; cursor:pointer; letter-spacing:.4px}
  button.run:hover{filter:brightness(1.07)}
  select, .ghost{background:var(--panel2); color:var(--ink); border:1px solid var(--line);
    border-radius:9px; padding:9px 12px; font-family:var(--mono); font-size:13px; cursor:pointer}
  .out{background:#0e0c0a; border:1px solid var(--line); border-radius:12px; padding:16px;
    white-space:pre-wrap; min-height:120px; font-size:15px; color:#e9e0cf}
  .out:empty::before{content:"— tu pojawi się wynik —"; color:var(--muted)}
  .hint{color:var(--muted); font-size:12px}
  @media (max-width:820px){ .wrap{grid-template-columns:1fr} aside{max-height:none} }
</style>
</head>
<body>
<header>
  <h1>EmoLang<span class="dot"> ●</span> IDE</h1>
  <p>Interpreter języka emoji — klikaj symbole z palety, nie musisz ich kopiować.</p>
</header>
<div class="wrap">
  <aside>
    {% for name, keys in palette %}
      <div class="grp">
        <h3>{{ name }}</h3>
        <div class="keys">
          {% for emoji, tip in keys %}
            <span class="key" onclick="insert('{{ emoji }} ')">{{ emoji }}<span class="tip">{{ tip }}</span></span>
          {% endfor %}
        </div>
      </div>
    {% endfor %}
  </aside>
  <main>
    <div class="row">
      <label>Program (.emo)</label>
      <div class="bar">
        <select id="ex" onchange="loadEx()">
          <option value="">— wczytaj przykład —</option>
          <option value="silnia">silnia (rekurencja)</option>
          <option value="lista">operacje na liście</option>
          <option value="wejscie">wczytywanie danych</option>
        </select>
        <span class="ghost" onclick="clearCode()">wyczyść</span>
      </div>
    </div>
    <textarea id="code" spellcheck="false" placeholder="📢 💬 Witaj! 💬 🔚"></textarea>

    <div>
      <label>Dane wejściowe (każda linia = jedno 📥)</label>
      <textarea id="stdin" spellcheck="false" placeholder="np. wartości czytane przez 📥, po jednej w linii"></textarea>
    </div>

    <div class="bar">
      <button class="run" onclick="runCode()">▶  Uruchom</button>
      <span class="hint">Skrót: Ctrl/⌘ + Enter</span>
    </div>

    <div>
      <label>Wynik</label>
      <div class="out" id="out"></div>
    </div>
  </main>
</div>

<script>
  const EXAMPLES = {{ examples_json | safe }};
  const code = document.getElementById('code');

  function insert(txt){
    const s = code.selectionStart, e = code.selectionEnd;
    code.value = code.value.slice(0,s) + txt + code.value.slice(e);
    code.selectionStart = code.selectionEnd = s + txt.length;
    code.focus();
  }
  function loadEx(){
    const v = document.getElementById('ex').value;
    if(v && EXAMPLES[v]){ code.value = EXAMPLES[v]; }
  }
  function clearCode(){ code.value=''; document.getElementById('out').textContent=''; code.focus(); }

  async function runCode(){
    const out = document.getElementById('out');
    out.textContent = 'Uruchamiam…';
    try{
      const r = await fetch('/run', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({code: code.value, stdin: document.getElementById('stdin').value})
      });
      const data = await r.json();
      out.textContent = data.output || '(program nic nie wypisał)';
    }catch(err){ out.textContent = 'Błąd połączenia: ' + err; }
  }
  document.addEventListener('keydown', e=>{
    if((e.ctrlKey||e.metaKey) && e.key==='Enter'){ e.preventDefault(); runCode(); }
  });
</script>
</body>
</html>"""


@app.route("/")
def index():
    import json
    return render_template_string(
        PAGE, palette=PALETTE, examples_json=json.dumps(EXAMPLES)
    )


@app.route("/run", methods=["POST"])
def run_route():
    data = request.get_json(force=True, silent=True) or {}
    output = run_capture(data.get("code", ""), data.get("stdin", ""))
    return jsonify(output=output)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
