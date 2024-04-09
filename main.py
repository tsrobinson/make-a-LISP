import sys
import reader
import printer
import mal_types
from env import Env
import core

def READ(x):
    return(reader.read_str(x))

def eval_ast(ast, repl_env):
    if isinstance(ast, mal_types.Symbol):
        try:
            return repl_env.get(ast.name)
        except KeyError:
            raise Exception(f"Could not find symbol {ast.name} not found in environment")
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
    
    while True:
    
        if not isinstance(x, list):
            return eval_ast(x, repl_env)
        elif x in []: # empty list
            return x
        else: # non-empty list
            if x.type == "list":
                
                if isinstance(x[0], mal_types.Symbol):
                    if x[0].name == "def!":
                        repl_env.set(x[1], EVAL(x[2], repl_env))
                        return mal_types.nil()
                        
                    elif x[0].name == "let*":
                        new_env = Env(repl_env, [], [])
                        bindings_list = x[1]
                        for i in range(0, len(bindings_list), 2):
                            new_env.set(bindings_list[i], EVAL(bindings_list[i+1], new_env))
                        repl_env = new_env
                        x = x[2]
                    
                    elif x[0].name == "do":
                        
                        for i in range(len(x[1])-1):
                            eval_ast(x[1][i], repl_env)
                        x = x[1][-1]
                    
                    elif x[0].name == "if":
                        cond = EVAL(x[1], repl_env)
                        if not isinstance(cond, mal_types.nil) and not isinstance(cond, mal_types.false):
                            x = x[2]
                        elif len(x) > 3:
                            x = x[3]
                        else:
                            return mal_types.nil()
                        
                    elif x[0].name == "fn*":
                        def new_fun(*args):
                            new_env = Env(repl_env, binds = [b.name for b in x[1]], exprs = args)
                            return EVAL(x[2], new_env)
                        
                        
                        return mal_types.Function(
                            x = x[2],
                            params = x[1],
                            env = repl_env,
                            fn = new_fun,
                        )
                    
                    else: 
                        eval_list = eval_ast(x, repl_env)
                        eval_0 = eval_list[0]
                        return eval_0(*eval_list[1:])
                
                else: # messy but needed to catch where x[0] is function not symbol
                    eval_list = eval_ast(x, repl_env)
                    f = eval_list[0]
                    x = f.x
                    new_env = Env(f.env, [b.name for b in f.params], eval_list[1:])
                    repl_env = new_env
            else:
                return eval_ast(x, repl_env)
            
def PRINT(x):
    return printer.pr_str(x)

def rep(x, repl_env):
    return PRINT(EVAL(READ(x), repl_env))

def main():
    
    base_env = Env(
        outer = mal_types.nil, 
        binds = core.ns.keys(), 
        exprs = list(core.ns.values()),
    )
    
    while True:
        try:
            user_in = input("user> ")
            if user_in == "quit":
                break
            elif user_in == "":
                continue
            else:
                print(rep(user_in, base_env))
        except EOFError:
            sys.exit()
        
if __name__ == "__main__":
    main()
