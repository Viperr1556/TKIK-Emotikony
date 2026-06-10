from ast_nodes import Environment, EmoError, ReturnSignal, FuncTemplate
from compiler import (PUSH_CONST, LOAD_VAR, STORE_VAR, POP,
                      ADD, SUB, MUL, DIV, EQ, NEQ, LT, GT, LE, GE,
                      NOT, NEG,
                      JUMP, JUMP_IF_FALSE, JUMP_IF_FALSE_OR_POP, JUMP_IF_TRUE_OR_POP,
                      MAKE_FUNC, CALL_FUNC, RETURN_VAL,
                      PRINT, INPUT, MAKE_LIST, INDEX, GET_LEN, APPEND_LIST,
                      CAST_NUM)


class Frame:
    """Ramka wywołania: bajtkod, wskaźnik instrukcji, stos, środowisko."""
    __slots__ = ('code', 'ip', 'stack', 'env')

    def __init__(self, code, env):
        self.code = code
        self.ip = 0
        self.stack = []
        self.env = env


class VM:
    """Maszyna stosowa wykonująca bajtkod EmoLang."""

    def run(self, code, env):
        f = Frame(code, env)
        stack = f.stack

        while f.ip < len(f.code):
            op, arg = f.code[f.ip]
            f.ip += 1

            # --- stałe i zmienne ---
            if   op == PUSH_CONST: stack.append(arg)
            elif op == LOAD_VAR:   stack.append(f.env.get(arg))
            elif op == STORE_VAR:  f.env.set(arg, stack.pop())
            elif op == POP:        stack.pop()

            # --- arytmetyka ---
            elif op == ADD:
                b, a = stack.pop(), stack.pop();  stack.append(a + b)
            elif op == SUB:
                b, a = stack.pop(), stack.pop();  stack.append(a - b)
            elif op == MUL:
                b, a = stack.pop(), stack.pop();  stack.append(a * b)
            elif op == DIV:
                b, a = stack.pop(), stack.pop()
                if b == 0: raise EmoError("próba dzielenia przez zero")
                stack.append(a / b)

            # --- porównania ---
            elif op == EQ:  b, a = stack.pop(), stack.pop(); stack.append(a == b)
            elif op == NEQ: b, a = stack.pop(), stack.pop(); stack.append(a != b)
            elif op == LT:  b, a = stack.pop(), stack.pop(); stack.append(a < b)
            elif op == GT:  b, a = stack.pop(), stack.pop(); stack.append(a > b)
            elif op == LE:  b, a = stack.pop(), stack.pop(); stack.append(a <= b)
            elif op == GE:  b, a = stack.pop(), stack.pop(); stack.append(a >= b)

            # --- logika i jednoargumentowe ---
            elif op == NOT: stack.append(not stack.pop())
            elif op == NEG: stack.append(-stack.pop())

            # --- skoki ---
            elif op == JUMP:
                f.ip = arg
            elif op == JUMP_IF_FALSE:
                if not stack.pop(): f.ip = arg
            elif op == JUMP_IF_FALSE_OR_POP:
                if not stack[-1]: f.ip = arg
                else: stack.pop()
            elif op == JUMP_IF_TRUE_OR_POP:
                if stack[-1]: f.ip = arg
                else: stack.pop()

            # --- funkcje ---
            elif op == MAKE_FUNC:
                name, params, body = arg
                f.env.set(name, FuncTemplate(name, params, body))

            elif op == CALL_FUNC:
                name, argc = arg
                func = f.env.get(name)
                if not isinstance(func, FuncTemplate):
                    raise EmoError(f"'{name}' nie jest funkcją")
                if argc != len(func.params):
                    raise EmoError(
                        f"funkcja '{name}' oczekuje {len(func.params)} "
                        f"argumentów, podano {argc}")
                vals = [stack.pop() for _ in range(argc)][::-1]
                local = Environment(parent=f.env.global_scope())
                for p, v in zip(func.params, vals):
                    local.set(p, v)
                try:
                    self.run(func.code, local)
                    stack.append(None)
                except ReturnSignal as ret:
                    stack.append(ret.value)

            elif op == RETURN_VAL:
                raise ReturnSignal(stack.pop())

            # --- wejście / wyjście ---
            elif op == PRINT:
                vals = [stack.pop() for _ in range(arg)][::-1]
                print(*vals)

            elif op == INPUT:
                try:    stack.append(input())
                except EOFError: stack.append("")

            # --- listy ---
            elif op == MAKE_LIST:
                items = [stack.pop() for _ in range(arg)][::-1]
                stack.append(items)

            elif op == INDEX:
                idx = int(stack.pop()); coll = stack.pop()
                try: stack.append(coll[idx])
                except IndexError: raise EmoError(f"indeks {idx} poza zakresem")

            elif op == GET_LEN:
                stack.append(len(stack.pop()))

            elif op == APPEND_LIST:
                val = stack.pop()
                lst = f.env.get(arg)
                if not isinstance(lst, list):
                    raise EmoError(f"'{arg}' nie jest listą")
                lst.append(val)

            # --- rzutowanie ---
            elif op == CAST_NUM:
                val = stack.pop()
                try:
                    txt = str(val).strip()
                    stack.append(float(txt) if '.' in txt else int(txt))
                except ValueError:
                    raise EmoError(f"nie można zamienić '{val}' na liczbę")
