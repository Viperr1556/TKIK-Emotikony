# Klasa Environment zarządza zasięgiem zmiennych (Globalne vs Lokalne)
class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent
        
    def set(self, name, value):
        self.vars[name] = value
        
    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        if self.parent:
            return self.parent.get(name)
        raise Exception(f"Zmienna '{name}' nie została zadeklarowana.")

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class Node:
    def eval(self, env): pass

class NumberNode(Node):
    def __init__(self, val): self.val = val
    def eval(self, env): return self.val

class StringNode(Node):
    def __init__(self, val): self.val = val
    def eval(self, env): return self.val

class ListNode(Node):
    def __init__(self, elements): self.elements = elements
    def eval(self, env): return [e.eval(env) for e in self.elements]

class VarNode(Node):
    def __init__(self, name): self.name = name
    def eval(self, env): return env.get(self.name)

class AssignNode(Node):
    def __init__(self, name, expr): self.name, self.expr = name, expr
    def eval(self, env):
        val = self.expr.eval(env)
        env.set(self.name, val)
        return val

class BinOpNode(Node):
    def __init__(self, left, op, right): self.left, self.op, self.right = left, op, right
    def eval(self, env):
        l = self.left.eval(env) if self.left else None
        r = self.right.eval(env)
        if self.op == '➕': return l + r
        if self.op == '➖': return l - r
        if self.op == '✖️': return l * r
        if self.op == '➗': return l / r
        if self.op == '⚖️': return l == r
        if self.op == '💔': return l != r
        if self.op == '👈': return l < r
        if self.op == '👉': return l > r
        if self.op == 'NOT': return not r
        return None

class BlockNode(Node):
    def __init__(self, stmts): self.stmts = stmts
    def eval(self, env):
        for s in self.stmts: s.eval(env)

class IfNode(Node):
    def __init__(self, cond, t_block, f_block=None): self.cond, self.t_block, self.f_block = cond, t_block, f_block
    def eval(self, env):
        if self.cond.eval(env): self.t_block.eval(env)
        elif self.f_block: self.f_block.eval(env)

class PrintNode(Node):
    def __init__(self, exprs): self.exprs = exprs
    def eval(self, env): print(*(e.eval(env) for e in self.exprs))

# --- Obsługa Funkcji ---
class FuncDefNode(Node):
    def __init__(self, name, params, body):
        self.name, self.params, self.body = name, params, body
    def eval(self, env):
        env.set(self.name, self)

class CallNode(Node):
    def __init__(self, name, args):
        self.name, self.args = name, args
    def eval(self, env):
        func = env.get(self.name)
        if not isinstance(func, FuncDefNode):
            raise Exception(f"'{self.name}' nie jest funkcją.")
        
        local_env = Environment(parent=env) # Zasięg lokalny
        eval_args = [a.eval(env) for a in self.args]
        
        for param_name, arg_val in zip(func.params, eval_args):
            local_env.set(param_name, arg_val)
            
        try:
            func.body.eval(local_env)
        except ReturnException as ret:
            return ret.value
        return None

class ReturnNode(Node):
    def __init__(self, expr): self.expr = expr
    def eval(self, env):
        raise ReturnException(self.expr.eval(env))
