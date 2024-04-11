from main import *

base_env = Env(
        outer = None, 
        binds = core.ns.keys(), 
        exprs = list(core.ns.values()),
    )
        
base_env.set(mal_types.Symbol("eval"), lambda a: EVAL(a, base_env))

rep("(def! not (fn* (a) (if a false true)))", base_env)

rep('''(def! load-file (fn* (f) (eval (read-string (str "(do " (slurp f) "\nnil)")))))''', base_env)

rep('(def! inc3 (fn* (a) (+ 3 a)))', base_env)

rep('(def! a (atom 2))', base_env)


rep('(atom? a)', base_env)


rep('(atom? 1)', base_env)

rep('(deref a)', base_env)


rep('(reset! a 3)', base_env)

rep('(deref a)', base_env)

rep('(swap! a inc3)', base_env)

x = READ('(swap! a inc3)')