# main.py
import sys
from parser_yacc import parser

def main():
    if len(sys.argv) < 2:
        print("Użycie: python main.py <plik.emo>")
        return

    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
        
        # Parsowanie i budowa drzewa AST
        ast = parser.parse(data)
        
        if ast:
            # Globalny kontekst zmiennych
            env = {}
            # Wykonanie programu
            ast.eval(env)
            
    except FileNotFoundError:
        print(f"Błąd: Nie znaleziono pliku '{filename}'")
    except Exception as e:
        print(f"Wystąpił krytyczny błąd: {e}")

if __name__ == "__main__":
    main()
