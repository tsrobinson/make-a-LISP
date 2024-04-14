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

rep('(def! nums (list 1 2 3))', repl_env)
rep('(def! double (fn* (a) (* 2 a)))', repl_env)

x = READ('(str "A" {:abc "val"} "Z")')
e = EVAL(x, repl_env)