import sys
import readline

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
            raise Exception(f"Symbol {ast.name} not in environment")
    elif isinstance(ast, list):
        if not isinstance(ast, mal_types.Array) or ast.type == "list":
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
        
        x = core.macroexpand(x, repl_env)
        
        if not isinstance(x, list):
            return eval_ast(x, repl_env)
        if x == []: # empty list
            return x
        
        if isinstance(x, mal_types.Array) and x.type in ['vector','hash-map']:
            return eval_ast(x, repl_env)
              
        elif isinstance(x[0], mal_types.Symbol) and x[0].name == "def!":
            return repl_env.set(x[1], EVAL(x[2], repl_env))
        
        elif isinstance(x[0], mal_types.Symbol) and x[0].name == "defmacro!":
            
            val = core._clone(EVAL(x[2], repl_env))
            if isinstance(val, mal_types.Function):
                val.is_macro = True
            
            return repl_env.set(x[1], val)
                
        elif isinstance(x[0], mal_types.Symbol) and x[0].name == "let*":
            new_env = Env(repl_env, [], [])
            bindings_list = x[1]
            for i in range(0, len(bindings_list), 2):
                new_env.set(bindings_list[i], EVAL(bindings_list[i+1], new_env))
            repl_env = new_env
            x = x[2]
        
        elif isinstance(x[0], mal_types.Symbol) and x[0].name == "do":
            
            eval_ast(x[1:-1], repl_env)
            x = x[-1]
        
        elif isinstance(x[0], mal_types.Symbol) and x[0].name == "if":
            cond = EVAL(x[1], repl_env)
            if not None and not isinstance(cond, mal_types.false):
                x = x[2]
            elif len(x) > 3:
                x = x[3]
            else:
                return None
            
        elif isinstance(x[0], mal_types.Symbol) and x[0].name == "fn*":
            def new_fun(*args):
                new_env = Env(repl_env, binds = [b.name for b in x[1]], exprs = args)
                return EVAL(x[2], new_env)
            
            return mal_types.Function(
                x = x[2],
                params = x[1],
                env = repl_env,
                fn = new_fun,
            )
            
        elif isinstance(x[0], mal_types.Symbol) and x[0].name == "quote":
            return x[1]
        
        elif isinstance(x[0], mal_types.Symbol) and x[0].name == "quasiquoteexpand":
            return core.quasiquote(x[1])
        
        elif isinstance(x[0], mal_types.Symbol) and x[0].name == "quasiquote":
            x = core.quasiquote(x[1])
            
        elif isinstance(x[0], mal_types.Symbol) and x[0].name == "macroexpand":
            return core.macroexpand(x[1], repl_env)
        
        elif isinstance(x[0], mal_types.Symbol) and x[0].name == "try*":
            
            try: 
                x = EVAL(x[1], repl_env)
            except Exception as e:
                if x[2][0] == mal_types.Symbol("catch*"):
                    new_env = Env(repl_env, [x[2][1].name], [e])
                    x = EVAL(x[2][2], new_env)
                else:
                    raise Exception("Invalid try* form")
               
        else: # list where first element is not a symbol i.e. a function/mal_types.Function
            eval_list = eval_ast(x, repl_env)
            if callable(eval_list[0]):
                eval_0 = eval_list[0]
                return eval_0(*eval_list[1:])
            else:
                f = eval_list[0]
                x = f.x
                new_env = Env(f.env, [b.name for b in f.params], eval_list[1:])
                repl_env = new_env
            
def PRINT(x):
    return printer.pr_str(x)

class CommentError(Exception):
    pass

def rep(x, repl_env):
    
    x = READ(x)
    if x is None:
        raise CommentError("")
    else:
        return PRINT(EVAL(x, repl_env))

def main():
    
    base_env = Env(
        outer = None, 
        binds = core.ns.keys(), 
        exprs = list(core.ns.values()),
    )
        
    base_env.set(mal_types.Symbol("eval"), lambda a: EVAL(a, base_env))
    base_env.set(mal_types.Symbol("*host-language*"), "Python 3.X")
    
    rep("(def! not (fn* (a) (if a false true)))", base_env)
    
    rep('(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) "\nnil)")))))', base_env)
    
    rep("(defmacro! cond (fn* (& xs) (if (> (count xs) 0) (list 'if (first xs) (if (> (count xs) 1) (nth xs 1) (throw \"odd number of forms to cond\")) (cons 'cond (rest (rest xs)))))))",
        base_env)
    
    if len(sys.argv) > 1:
        
        rep(f"(def! *ARGV* (list {''.join([f'{x}' for x in sys.argv[2:]])}))", base_env)
        rep(f'(load-file "{sys.argv[1]}")', base_env)
        exit()
        
    _run = True
    rep('(println (str "Mal [" *host-language* "]"))', base_env)
    while _run:
        
        try:
            user_in = input("user> ")
            if user_in == "quit":
                break
            elif user_in == "":
                continue
            else:
                out = rep(user_in, base_env)
                print(out)
        except EOFError:
            sys.exit()
        except CommentError:
            continue
        
if __name__ == "__main__":
    main()
