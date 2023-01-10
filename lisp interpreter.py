import operator

def eval_expr(expr, env):
    if isinstance(expr, (int, float)):
        return expr
    if isinstance(expr, str):
        return env[expr]
    if not isinstance(expr, list):
        raise ValueError(f"Invalid expression: {expr}")

    op, *args = expr
    if op == 'define':
        var, val = args
        env[var] = eval_expr(val, env)
    elif op == 'lambda':
        params, body = args
        return lambda *args: eval_expr(body, dict(zip(params, args)))
    else:
        op = eval_expr(op, env)
        args = [eval_expr(arg, env) for arg in args]
        return op(*args)

def parse(input_str):
    input_str = input_str.strip()
    if not input_str:
        return []
    if input_str[0] != '(':
        return input_str
    tokens = input_str[1:].split()
    res = []
    for token in tokens:
        if token == '(':
            res.append(parse(input_str[1:]))
        elif token == ')':
            return res
        else:
            res.append(token)
    return res

def repl(env):
    while True:
        input_str = input("lisp> ")
        if not input_str:
            continue
        if input_str.lower() in ('exit', 'quit'):
            break
        try:
            expr = parse(input_str)
            result = eval_expr(expr, env)
            if result is not None:
                print(result)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    env = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv,
        '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '=': operator.eq
    }
    repl(env)
