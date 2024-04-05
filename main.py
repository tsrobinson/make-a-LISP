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
    '/': lambda a,b: a/b,
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
        return [EVAL(x, repl_env) for x in ast]
    else:
        return ast

def EVAL(x, repl_env):
    if not isinstance(x, list):
        return(eval_ast(x, repl_env))
    else:
        if x == []:
            return(x)
        else:
            eval_list = eval_ast(x, repl_env)
            eval_0 = eval_list[0]
            return(eval_0(*eval_list[1:]))
            
def PRINT(x):
    return(printer.pr_str(x))

def rep(x):
    return(PRINT(EVAL(READ(x), repl_env)))

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