from mal_types import true, false, Array, Symbol, atom
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
    
def quasiquote(x):
    if isinstance(x, Array) and len(x) > 0 and isinstance(x[0], Symbol) and x[0].name == "unquote":
        return x[1]
    elif isinstance(x, Array) and x.type == "list":
        res = Array([],"(")
        for elt in reversed(x):
            if isinstance(elt, Array) and len(elt) > 0 and isinstance(elt[0], Symbol) and elt[0].name == "splice-unquote":
                res = Array([Symbol("concat"), elt[1], res],"(")
            else:
                res= Array([Symbol("cons"), quasiquote(elt), res], "(")
        return Array(res, "(")
    else:
        return Array([Symbol("quote"), x], "(")

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
    
}


