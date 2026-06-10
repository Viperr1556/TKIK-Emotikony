

from ast_nodes import *

# --- Kody operacji (bajtkod) ---

PUSH_CONST  = 1   # połóż stałą na stosie
LOAD_VAR    = 2   # połóż wartość zmiennej na stosie
STORE_VAR   = 3   # zdejmij ze stosu i zapisz do zmiennej
POP         = 4   # odrzuć wierzchołek stosu

ADD  = 10;  SUB = 11;  MUL = 12;  DIV = 13
EQ   = 14;  NEQ = 15;  LT  = 16;  GT  = 17;  LE = 18;  GE = 19
NOT  = 20;  NEG = 21

JUMP                 = 30  # skok bezwarunkowy
JUMP_IF_FALSE        = 31  # zdejmij; jeśli fałsz — skocz
JUMP_IF_FALSE_OR_POP = 32  # jeśli fałsz — zostaw i skocz; jeśli prawda — zdejmij
JUMP_IF_TRUE_OR_POP  = 33  # jeśli prawda — zostaw i skocz; jeśli fałsz — zdejmij

MAKE_FUNC  = 40  # zdefiniuj funkcję (zapisz FuncTemplate)
CALL_FUNC  = 41  # wywołaj funkcję
RETURN_VAL = 42  # zwróć wartość z funkcji

PRINT      = 50  # wypisz N wartości ze stosu
INPUT      = 51  # wczytaj linię, połóż na stosie

MAKE_LIST  = 60  # utwórz listę z N elementów ze stosu
INDEX      = 61  # pobierz element listy
GET_LEN    = 62  # długość listy/tekstu
APPEND_LIST = 63 # dopnij element do listy

CAST_NUM   = 70  # zamień na liczbę

# mapowanie nazw operatorów z parsera na kody bajtkodu
_binop = {
    'PLUS': ADD, 'MINUS': SUB, 'TIMES': MUL, 'DIVIDE': DIV,
    'EQ': EQ, 'NEQ': NEQ, 'LT': LT, 'GT': GT, 'LE': LE, 'GE': GE,
}

# typy węzłów, które kładą wartość na stos (wyrażenia)
_pushes = (NumberNode, StringNode, BoolNode, ListNode, VarNode,
           BinOpNode, UnaryOpNode, IndexNode, LenNode, CastNode,
           InputNode, CallNode)

# nazwy kodów — do wyświetlania bajtkodu (disassemble)
_opname = {
    PUSH_CONST: 'PUSH_CONST', LOAD_VAR: 'LOAD_VAR', STORE_VAR: 'STORE_VAR',
    POP: 'POP', ADD: 'ADD', SUB: 'SUB', MUL: 'MUL', DIV: 'DIV',
    EQ: 'EQ', NEQ: 'NEQ', LT: 'LT', GT: 'GT', LE: 'LE', GE: 'GE',
    NOT: 'NOT', NEG: 'NEG',
    JUMP: 'JUMP', JUMP_IF_FALSE: 'POP_JUMP_FALSE',
    JUMP_IF_FALSE_OR_POP: 'JUMP_FALSE_OR_POP',
    JUMP_IF_TRUE_OR_POP: 'JUMP_TRUE_OR_POP',
    MAKE_FUNC: 'MAKE_FUNC', CALL_FUNC: 'CALL_FUNC', RETURN_VAL: 'RETURN_VAL',
    PRINT: 'PRINT', INPUT: 'INPUT',
    MAKE_LIST: 'MAKE_LIST', INDEX: 'INDEX', GET_LEN: 'GET_LEN',
    APPEND_LIST: 'APPEND_LIST', CAST_NUM: 'CAST_NUM',
}


class Compiler:
    def __init__(self):
        self.code = []

    def emit(self, op, arg=None):
        self.code.append((op, arg))
        return len(self.code) - 1

    def patch_jump(self, addr):
        """Uzupełnij adres skoku (znany dopiero po skompilowaniu bloku)."""
        op, _ = self.code[addr]
        self.code[addr] = (op, len(self.code))

    # --- Kompilacja poszczególnych węzłów ---

    def compile(self, node):
        t = type(node)

        if t is BlockNode:
            for stmt in node.statements:
                self.compile(stmt)
                if isinstance(stmt, _pushes):
                    self.emit(POP)

        elif t is NumberNode:  self.emit(PUSH_CONST, node.value)
        elif t is StringNode:  self.emit(PUSH_CONST, node.value)
        elif t is BoolNode:    self.emit(PUSH_CONST, node.value)

        elif t is ListNode:
            for el in node.elements:
                self.compile(el)
            self.emit(MAKE_LIST, len(node.elements))

        elif t is VarNode:
            self.emit(LOAD_VAR, node.name)

        elif t is AssignNode:
            self.compile(node.expr)
            self.emit(STORE_VAR, node.name)

        elif t is BinOpNode:
            if node.op == 'AND':
                self.compile(node.left)
                j = self.emit(JUMP_IF_FALSE_OR_POP)
                self.compile(node.right)
                self.patch_jump(j)
            elif node.op == 'OR':
                self.compile(node.left)
                j = self.emit(JUMP_IF_TRUE_OR_POP)
                self.compile(node.right)
                self.patch_jump(j)
            else:
                self.compile(node.left)
                self.compile(node.right)
                self.emit(_binop[node.op])

        elif t is UnaryOpNode:
            self.compile(node.expr)
            self.emit(NEG if node.op == 'NEG' else NOT)

        elif t is IfNode:
            self.compile(node.cond)
            j_else = self.emit(JUMP_IF_FALSE)
            self.compile(node.then_block)
            if node.else_block:
                j_end = self.emit(JUMP)
                self.patch_jump(j_else)
                self.compile(node.else_block)
                self.patch_jump(j_end)
            else:
                self.patch_jump(j_else)

        elif t is WhileNode:
            loop_top = len(self.code)
            self.compile(node.cond)
            j_end = self.emit(JUMP_IF_FALSE)
            self.compile(node.block)
            self.emit(JUMP, loop_top)
            self.patch_jump(j_end)

        elif t is PrintNode:
            for expr in node.exprs:
                self.compile(expr)
            self.emit(PRINT, len(node.exprs))

        elif t is InputNode:
            self.emit(INPUT)

        elif t is CastNode:
            self.compile(node.expr)
            self.emit(CAST_NUM)

        elif t is IndexNode:
            self.compile(node.collection)
            self.compile(node.index)
            self.emit(INDEX)

        elif t is LenNode:
            self.compile(node.expr)
            self.emit(GET_LEN)

        elif t is AppendNode:
            self.compile(node.expr)
            self.emit(APPEND_LIST, node.name)

        elif t is FuncDefNode:
            body = Compiler()
            body.compile(node.body)
            self.emit(MAKE_FUNC, (node.name, node.params, body.code))

        elif t is CallNode:
            for a in node.args:
                self.compile(a)
            self.emit(CALL_FUNC, (node.name, len(node.args)))

        elif t is ReturnNode:
            self.compile(node.expr)
            self.emit(RETURN_VAL)

        else:
            raise EmoError(f"nieznany węzeł: {t.__name__}")


def compile_ast(ast):
    """Kompiluje drzewo AST do bajtkodu."""
    c = Compiler()
    c.compile(ast)
    return c.code


def disassemble(code, indent=0):
    """Zwraca czytelny tekst z listą instrukcji bajtkodu."""
    pad = "  " * indent
    lines = []
    for i, (op, arg) in enumerate(code):
        name = _opname.get(op, f'?{op}')
        if op == MAKE_FUNC:
            fname, params, body = arg
            lines.append(f"{pad}{i:4d}  {name:22s} {fname}({', '.join(params)})")
            lines.append(disassemble(body, indent + 1))
        elif arg is not None:
            lines.append(f"{pad}{i:4d}  {name:22s} {arg}")
        else:
            lines.append(f"{pad}{i:4d}  {name}")
    return "\n".join(lines)
