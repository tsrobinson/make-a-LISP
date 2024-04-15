import re
from main import *
from mal_types import true, false, Array, Symbol, atom

base_env = Env(
        outer = None, 
        binds = core.ns.keys(), 
        exprs = list(core.ns.values()),
    )
        
base_env.set(mal_types.Symbol("eval"), lambda a: EVAL(a, base_env))

rep("(def! not (fn* (a) (if a false true)))", base_env)

rep('''(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) "\nnil)")))))''', base_env)

rep('''(def! c (quote (1 "b" "d")))''', base_env)

repl_env = base_env

str_in = rep('''(str "(do " (slurp "tests/computations.mal") "\nnil)"))''', repl_env)
t = reader.tokenize(str_in)


str_in = rep('''(read-string (str "(do " (slurp "tests/computations.mal") "\nnil)")))''', repl_env)



x = rep('''(eval (read-string (str "(do " (slurp "tests/computations.mal") "\nnil)")))''', repl_env)
