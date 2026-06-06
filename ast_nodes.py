# -*- coding: utf-8 -*-
"""
EmoLang - węzły drzewa składniowego (AST) + interpreter.

To jest serce INTERPRETERA. Parser buduje z programu drzewo obiektów (AST).
Każdy obiekt to jeden rodzaj konstrukcji języka i ma metodę `eval(env)`,
która OD RAZU WYKONUJE tę konstrukcję (nie tłumaczymy nic na Pythona ani na
inny język - po prostu chodzimy po drzewie i liczymy wynik).

Taki sposób wykonywania nazywa się "tree-walking interpreter".

Ważne: w tym pliku NIE MA ani jednego emoji. Emoji żyją tylko w lekserze.
Parser zamienia je na nazwy tokenów ('PLUS', 'LT', ...), a tutaj operujemy
już wyłącznie na tych nazwach. To utrzymuje warstwy rozdzielone i czytelne.
"""


class EmoError(Exception):
    """Błąd wykonania programu EmoLang (np. dzielenie przez zero)."""
    pass


# ===========================================================================
# Środowisko = pamięć zmiennych (z obsługą zakresów: globalny + lokalne funkcji)
# ===========================================================================

class Environment:
    def __init__(self, parent=None):
        self.vars = {}          # zmienne widoczne w tym zakresie
        self.parent = parent    # zakres nadrzędny (None dla globalnego)

    def set(self, name, value):
        self.vars[name] = value

    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent is not None:
            return self.parent.get(name)
        raise EmoError(f"zmienna '{name}' nie została zadeklarowana")

    def global_scope(self):
        """Zwraca najwyższy (globalny) zakres - idąc po rodzicach do góry."""
        env = self
        while env.parent is not None:
            env = env.parent
        return env


class ReturnSignal(Exception):
    """Wewnętrzny sygnał: instrukcja 'zwróć' przerywa funkcję i niesie wynik."""
    def __init__(self, value):
        self.value = value


# ===========================================================================
# Bazowy węzeł
# ===========================================================================

class Node:
    def eval(self, env):
        raise NotImplementedError


# ===========================================================================
# Wartości stałe (liczby, teksty, logika, listy)
# ===========================================================================

class NumberNode(Node):
    def __init__(self, value): self.value = value
    def eval(self, env): return self.value

class StringNode(Node):
    def __init__(self, value): self.value = value
    def eval(self, env): return self.value

class BoolNode(Node):
    def __init__(self, value): self.value = value
    def eval(self, env): return self.value

class ListNode(Node):
    def __init__(self, elements): self.elements = elements
    def eval(self, env): return [e.eval(env) for e in self.elements]


# ===========================================================================
# Zmienne
# ===========================================================================

class VarNode(Node):
    """Odczyt wartości zmiennej."""
    def __init__(self, name): self.name = name
    def eval(self, env): return env.get(self.name)

class AssignNode(Node):
    """Przypisanie: name 📦 expr"""
    def __init__(self, name, expr):
        self.name, self.expr = name, expr
    def eval(self, env):
        value = self.expr.eval(env)
        env.set(self.name, value)
        return value


# ===========================================================================
# Operatory
# ===========================================================================

class BinOpNode(Node):
    """Operator dwuargumentowy. `op` to NAZWA tokenu, np. 'PLUS', 'LT'."""
    def __init__(self, left, op, right):
        self.left, self.op, self.right = left, op, right

    def eval(self, env):
        op = self.op
        left = self.left.eval(env)

        # operatory logiczne - z "leniwym" (short-circuit) wartościowaniem
        if op == 'AND':
            return left if not left else self.right.eval(env)
        if op == 'OR':
            return left if left else self.right.eval(env)

        right = self.right.eval(env)

        if op == 'PLUS':   return left + right
        if op == 'MINUS':  return left - right
        if op == 'TIMES':  return left * right
        if op == 'DIVIDE':
            if right == 0:
                raise EmoError("próba dzielenia przez zero")
            return left / right
        if op == 'EQ':  return left == right
        if op == 'NEQ': return left != right
        if op == 'LT':  return left < right
        if op == 'GT':  return left > right
        if op == 'LE':  return left <= right
        if op == 'GE':  return left >= right
        raise EmoError(f"nieznany operator '{op}'")


class UnaryOpNode(Node):
    """Operator jednoargumentowy: 'NOT' (negacja logiczna) lub 'NEG' (minus)."""
    def __init__(self, op, expr):
        self.op, self.expr = op, expr
    def eval(self, env):
        value = self.expr.eval(env)
        if self.op == 'NOT': return not value
        if self.op == 'NEG': return -value
        raise EmoError(f"nieznany operator jednoargumentowy '{self.op}'")


# ===========================================================================
# Bloki i sterowanie
# ===========================================================================

class BlockNode(Node):
    """Ciąg instrukcji. None-y (np. po samym 🔚) są odfiltrowywane."""
    def __init__(self, statements):
        self.statements = [s for s in statements if s is not None]
    def eval(self, env):
        for stmt in self.statements:
            stmt.eval(env)

class IfNode(Node):
    def __init__(self, cond, then_block, else_block=None):
        self.cond, self.then_block, self.else_block = cond, then_block, else_block
    def eval(self, env):
        if self.cond.eval(env):
            self.then_block.eval(env)
        elif self.else_block is not None:
            self.else_block.eval(env)

class WhileNode(Node):
    def __init__(self, cond, block):
        self.cond, self.block = cond, block
    def eval(self, env):
        while self.cond.eval(env):
            self.block.eval(env)


# ===========================================================================
# Wejście / wyjście
# ===========================================================================

class PrintNode(Node):
    def __init__(self, exprs): self.exprs = exprs
    def eval(self, env):
        print(*[e.eval(env) for e in self.exprs])

class InputNode(Node):
    def eval(self, env):
        try:
            return input()        # zawsze zwraca tekst (string)
        except EOFError:
            return ""


# ===========================================================================
# Rzutowanie typów
# ===========================================================================

class CastNode(Node):
    """🔢 = zamień tekst na liczbę (int gdy całkowity, inaczej float)."""
    def __init__(self, expr):
        self.expr = expr
    def eval(self, env):
        value = self.expr.eval(env)
        try:
            text = str(value).strip()
            return float(text) if '.' in text else int(text)
        except ValueError:
            raise EmoError(f"nie można zamienić '{value}' na liczbę")


# ===========================================================================
# Operacje na listach
# ===========================================================================

class IndexNode(Node):
    """expr 🎯 index  -> element listy/tekstu pod indeksem."""
    def __init__(self, collection, index):
        self.collection, self.index = collection, index
    def eval(self, env):
        coll = self.collection.eval(env)
        idx = int(self.index.eval(env))
        try:
            return coll[idx]
        except IndexError:
            raise EmoError(f"indeks {idx} poza zakresem")

class LenNode(Node):
    """📏 expr  -> długość listy lub tekstu."""
    def __init__(self, expr): self.expr = expr
    def eval(self, env): return len(self.expr.eval(env))

class AppendNode(Node):
    """name 🖇️ expr  -> dopina wartość na koniec listy o nazwie `name`."""
    def __init__(self, name, expr):
        self.name, self.expr = name, expr
    def eval(self, env):
        lst = env.get(self.name)
        if not isinstance(lst, list):
            raise EmoError(f"'{self.name}' nie jest listą")
        value = self.expr.eval(env)
        lst.append(value)
        return value


# ===========================================================================
# Funkcje
# ===========================================================================

class FuncDefNode(Node):
    """Definicja funkcji. eval() zapisuje samą funkcję w środowisku."""
    def __init__(self, name, params, body):
        self.name, self.params, self.body = name, params, body
    def eval(self, env):
        env.set(self.name, self)

class CallNode(Node):
    """Wywołanie funkcji: 📞 name ( args )."""
    def __init__(self, name, args):
        self.name, self.args = name, args
    def eval(self, env):
        func = env.get(self.name)
        if not isinstance(func, FuncDefNode):
            raise EmoError(f"'{self.name}' nie jest funkcją")
        if len(self.args) != len(func.params):
            raise EmoError(f"funkcja '{self.name}' oczekuje {len(func.params)} "
                           f"argumentów, podano {len(self.args)}")
        # Argumenty liczymy w środowisku WYWOŁANIA...
        values = [a.eval(env) for a in self.args]
        # ...ale ciało wykonujemy w świeżym zakresie, którego rodzicem jest
        # zakres globalny (funkcja widzi globalne + własne parametry).
        local = Environment(parent=env.global_scope())
        for param, value in zip(func.params, values):
            local.set(param, value)
        try:
            func.body.eval(local)
        except ReturnSignal as ret:
            return ret.value
        return None

class ReturnNode(Node):
    def __init__(self, expr): self.expr = expr
    def eval(self, env):
        raise ReturnSignal(self.expr.eval(env))
