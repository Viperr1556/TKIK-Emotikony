import sys
from parser_yacc import parser
from ast_nodes import Environment

def run_interpreter(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
            
        ast = parser.parse(code)
        
        if ast:
            global_env = Environment()
            ast.eval(global_env)
            
    except Exception as e:
        print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_interpreter(sys.argv[1])
    else:
        print("Użycie: python main.py <program.emo>")
