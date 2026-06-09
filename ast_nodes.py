# -*- coding: utf-8 -*-
"""Węzły drzewa składniowego (AST), środowisko zmiennych, typy pomocnicze.

Węzły to czyste kontenery danych — nie mają logiki wykonania.
Wykonaniem zajmuje się maszyna wirtualna (vm.py) na podstawie
bajtkodu wygenerowanego przez kompilator (compiler.py).
"""


class EmoError(Exception):
    """Błąd wykonania programu EmoLang."""
    pass


class Environment:
    """Pamięć zmiennych z obsługą zakresów (globalny + lokalne funkcji)."""
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def set(self, name, value):
        self.vars[name] = value

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise EmoError(f"zmienna '{name}' nie została zadeklarowana")

    def global_scope(self):
        env = self
        while env.parent is not None:
            env = env.parent
        return env


class ReturnSignal(Exception):
    """Sygnał wewnętrzny: return przerywa funkcję i niesie wynik."""
    def __init__(self, value):
        self.value = value


class FuncTemplate:
    """Skompilowana funkcja: nazwa, parametry i bajtkod ciała."""
    def __init__(self, name, params, code):
        self.name, self.params, self.code = name, params, code


# --- Węzły AST (czyste dane, bez logiki) ---

class Node: pass

class NumberNode(Node):
    def __init__(self, value): self.value = value

class StringNode(Node):
    def __init__(self, value): self.value = value

class BoolNode(Node):
    def __init__(self, value): self.value = value

class ListNode(Node):
    def __init__(self, elements): self.elements = elements

class VarNode(Node):
    def __init__(self, name): self.name = name

class AssignNode(Node):
    def __init__(self, name, expr):
        self.name, self.expr = name, expr

class BinOpNode(Node):
    def __init__(self, left, op, right):
        self.left, self.op, self.right = left, op, right

class UnaryOpNode(Node):
    def __init__(self, op, expr):
        self.op, self.expr = op, expr

class BlockNode(Node):
    def __init__(self, statements):
        self.statements = [s for s in statements if s is not None]

class IfNode(Node):
    def __init__(self, cond, then_block, else_block=None):
        self.cond, self.then_block, self.else_block = cond, then_block, else_block

class WhileNode(Node):
    def __init__(self, cond, block):
        self.cond, self.block = cond, block

class PrintNode(Node):
    def __init__(self, exprs): self.exprs = exprs

class InputNode(Node):
    pass

class CastNode(Node):
    def __init__(self, expr): self.expr = expr

class IndexNode(Node):
    def __init__(self, collection, index):
        self.collection, self.index = collection, index

class LenNode(Node):
    def __init__(self, expr): self.expr = expr

class AppendNode(Node):
    def __init__(self, name, expr):
        self.name, self.expr = name, expr

class FuncDefNode(Node):
    def __init__(self, name, params, body):
        self.name, self.params, self.body = name, params, body

class CallNode(Node):
    def __init__(self, name, args):
        self.name, self.args = name, args

class ReturnNode(Node):
    def __init__(self, expr): self.expr = expr
