# ast_nodes.py

class Node:
    def eval(self, env):
        raise NotImplementedError

class NumberNode(Node):
    def __init__(self, value):
        self.value = value
    def eval(self, env):
        return self.value

class StringNode(Node):
    def __init__(self, value):
        self.value = value
    def eval(self, env):
        return self.value

class BooleanNode(Node):
    def __init__(self, value):
        self.value = value
    def eval(self, env):
        return self.value

class VarNode(Node):
    def __init__(self, name):
        self.name = name
    def eval(self, env):
        if self.name in env:
            return env[self.name]
        print(f"🔥 Błąd wykonania: Zmienna '{self.name}' nie jest zdefiniowana.")
        return 0

class AssignNode(Node):
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
    def eval(self, env):
        value = self.expr.eval(env)
        env[self.name] = value
        return value

class BinOpNode(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def eval(self, env):
        l_val = self.left.eval(env)
        r_val = self.right.eval(env)
        if self.op == '➕': return l_val + r_val
        if self.op == '➖': return l_val - r_val
        if self.op == '✖️': return l_val * r_val
        if self.op == '➗': 
            if r_val == 0: 
                print("🔥 Błąd: Dzielenie przez zero!")
                return 0
            return l_val / r_val
        # Operatory porównania
        if self.op == '⚖️': return l_val == r_val
        if self.op == '💔': return l_val != r_val
        if self.op == '👈': return l_val < r_val
        if self.op == '👉': return l_val > r_val
        return 0

class PrintNode(Node):
    def __init__(self, expr):
        self.expr = expr
    def eval(self, env):
        result = self.expr.eval(env)
        print(result)

class BlockNode(Node):
    def __init__(self, statements):
        self.statements = statements
    def eval(self, env):
        result = None
        for stmt in self.statements:
            result = stmt.eval(env)
        return result

class IfNode(Node):
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block
    def eval(self, env):
        if self.condition.eval(env):
            return self.true_block.eval(env)
        elif self.false_block:
            return self.false_block.eval(env)
