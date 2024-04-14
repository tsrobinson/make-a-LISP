from mal_types import true, false, Array, Symbol, atom, Function 
from printer import pr_str
from reader import read_str

def prn(*args):
    print(" ".join([pr_str(x) for x in args]))
    return None

def println(*args):
    print(" ".join([pr_str(x, print_readably=False) for x in args]))
    return None

def reset_atom(a, val):
    a.reference = val
    return a.reference

def swap_atom(a, f, *args):
       
    if callable(f):
        a.reference = f(a.reference, *args)
    else:
        a.reference = f.fn(a.reference, *args)
    return a.reference

def _qq_expand(x):
    res = Array([],"(")
    for elt in reversed(x):
        if isinstance(elt, Array) and len(elt) > 0 and isinstance(elt[0], Symbol) and elt[0].name == "splice-unquote":
            res = Array([Symbol("concat"), elt[1], res],"(")
        else:
            res= Array([Symbol("cons"), quasiquote(elt), res], "(")
    return Array(res, "(")
    
def quasiquote(x):
    if isinstance(x, Array) and x.type == "vector":
        return Array([Symbol("vec"), _qq_expand(Array(x,"("))],"(")
    elif isinstance(x, Array) and len(x) > 0 and isinstance(x[0], Symbol) and x[0].name == "unquote":
        return x[1]
    elif isinstance(x, Array) and x.type == "list":
        return _qq_expand(x)
    elif isinstance(x, Array) and x.type == "hash-map" or isinstance(x, Symbol):
        return Array([Symbol("quote"), x], "(")
    else:
        return x
    
def is_macro_call(x, env):
    
    if not isinstance(x, Array):
        call = False
    elif x.type != "list" or len(x) < 1:
        call = False
    elif not isinstance(x[0], Symbol):
        call = False
    elif env.find(x[0].name) is None:
        call = False
    elif not isinstance(env.get(x[0].name), Function):
        call = False
    elif not env.get(x[0].name).is_macro:
        call = False
    else:
        call = True
    
    return call

def macroexpand(x, env):
    
    while is_macro_call(x, env):
        macro = env.get(x[0].name)
        x = macro.fn(*x[1:])
        
    return x


ns = {
    '+': lambda a,b: a+b,
    '-': lambda a,b: a-b,
    '*': lambda a,b: a*b,
    '/': lambda a,b: int(a/b),
    
    '=': lambda a,b: true() if a==b else false(),
    '<': lambda a,b: true() if a<b else false(),
    '<=': lambda a,b: true() if a<=b else false(),
    '>': lambda a,b: true() if a>b else false(),
    '>=': lambda a,b: true() if a>=b else false(),
    
    'list': lambda *args: Array(args, "("),
    'list?': lambda *args:true() if isinstance(args[0], list) else false(),
    'empty?': lambda *args: true() if args[0] == [] else false(),
    'count': lambda *args: len(args[0]),
       
    'prn': prn,
    'pr-str': lambda *args: "".join([pr_str(x, print_readably=True) for x in args]),
    'str': lambda *args: "".join([pr_str(x, print_readably=False) for x in args]),
    'println': lambda *args: println(*args),
    
    'read-string': lambda a: read_str(a),
    'slurp': lambda a: open(a, "r").read(),
    
    
    'atom': lambda val: atom(val),
    'atom?': lambda a: true() if isinstance(a, atom) else false(),
    'deref': lambda a: a.reference,
    'reset!': reset_atom,
    'swap!': swap_atom,
    
    'cons': lambda a,b: Array([a]+b,"("),
    'concat': lambda *args: Array([x for y in args for x in y], "("),
    
    'vec': lambda a: Array(a, "["),
    
}


