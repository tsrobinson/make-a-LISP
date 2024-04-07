import sys
import reader
import printer
import mal_types

def READ(x):
    return(reader.read_str(x))

repl_env = {
    '+': lambda a,b: a+b,
    '-': lambda a,b: a-b,
    '*': lambda a,b: a*b,
    '/': lambda a,b: int(a/b),
    '%': lambda a,b: a-int(a/b)*b,
    '^': lambda a,b: a**b,
}

def eval_ast(ast, repl_env):
    if isinstance(ast, mal_types.Symbol):
        try:
            return repl_env[ast.name]
        except KeyError:
            raise Exception(f"Symbol {ast.name} not found in environment")
    elif isinstance(ast, list):
        if ast.type == "list":
            return mal_types.Array([EVAL(x, repl_env) for x in ast], "(")
        elif ast.type == "vector":
            return mal_types.Array([EVAL(x, repl_env) for x in ast], "[")
        elif ast.type == "hash-map":
            return mal_types.Array([EVAL(x, repl_env) for x in ast], "{")
        else:
            raise ValueError("Invalid array type")
    else:
        return ast

def EVAL(x, repl_env):
    if not isinstance(x, list):
        return eval_ast(x, repl_env)
    elif x in []: # empty list
        return(x)
    else: # non-empty list
        eval_list = eval_ast(x, repl_env)
        if x.type == "list":
            eval_0 = eval_list[0]
            return eval_0(*eval_list[1:])
        else:
            return eval_ast(x, repl_env)

def PRINT(x):
    return printer.pr_str(x)

def rep(x):
    return PRINT(EVAL(READ(x), repl_env))

def main():
    
    while True:
        try:
            user_in = input("user> ")
            res = rep(user_in)
            print(res)
        except EOFError:
            sys.exit()
        
if __name__ == "__main__":
    main()