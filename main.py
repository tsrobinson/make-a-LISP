import sys
import reader
import printer
import mal_types
from env import Env

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
    if not isinstance(x, list):
        return eval_ast(x, repl_env)
    elif x in []: # empty list
        return x
    else: # non-empty list
        if x.type == "list":
            
            if isinstance(x[0], mal_types.Symbol):
                if x[0].name == "def!":
                    repl_env.set(x[1], EVAL(x[2], repl_env))
                    
                elif x[0].name == "let*":
                    new_env = Env(repl_env, [], [])
                    bindings_list = x[1]
                    for i in range(0, len(bindings_list), 2):
                        new_env.set(bindings_list[i], EVAL(bindings_list[i+1], new_env))
                    return EVAL(x[2], new_env)
                
                elif x[0].name == "do":
                    """
                    Evaluate all the elements of the list using eval_ast and return the final evaluated element.
                    """
                    return [eval_ast(y, repl_env) for y in x[1]][-1]
                
                elif x[0].name == "if":
                    """
                    Evaluate the first parameter (second element). If the result (condition) is anything other
                    than nil or false, then evaluate the second parameter (third element of the list) and return
                    the result. Otherwise, evaluate the third parameter (fourth element) and return the result. 
                    If condition is false and there is no third parameter, then just return nil.
                    """
                    
                    cond = EVAL(x[1], repl_env)
                    if not isinstance(cond, mal_types.nil) and not isinstance(cond, mal_types.false):
                        return EVAL(x[2], repl_env)
                    elif len(x) > 3:
                        return EVAL(x[3], repl_env)
                    else:
                        return mal_types.nil()
                    
                elif x[0].name == "fn*":
                    """
                    Return a new function closure. 
                    The body of that closure does the following:
                        Create a new environment using env (closed over from outer scope) as the outer parameter,
                        the first parameter (second list element of ast from the outer scope) as the binds parameter,
                        and the parameters to the closure as the exprs parameter.
                        
                        Call EVAL on the second parameter (third list element of ast from outer scope), using the new 
                        environment. Use the result as the return value of the closure.
                    """
                    
                    def new_fun(*args):
                        new_env = Env(repl_env, binds = [b.name for b in x[1]], exprs = args)
                        return EVAL(x[2], new_env)
                    
                    return new_fun
                
                else: 
                    eval_list = eval_ast(x, repl_env)
                    eval_0 = eval_list[0]
                    return eval_0(*eval_list[1:])
            
            else: # messy but needed to catch where [0] is function not symbol
                eval_list = eval_ast(x, repl_env)
                eval_0 = eval_list[0]
                return eval_0(*eval_list[1:])
        else:
            return eval_ast(x, repl_env)

def PRINT(x):
    return printer.pr_str(x)

def rep(x, repl_env):
    return PRINT(EVAL(READ(x), repl_env))

def main():
    
    init_binds = ['+','-','*','/']
    init_exprs = [lambda a,b: a+b, lambda a,b: a-b, lambda a,b: a*b, lambda a,b: int(a/b)]

    base_env = Env(
        outer = mal_types.nil, 
        binds = init_binds, 
        exprs = init_exprs
    )
    
    while True:
        try:
            user_in = input("user> ")
            res = rep(user_in, base_env)
            print(res)
        except EOFError:
            sys.exit()
        
if __name__ == "__main__":
    main()
