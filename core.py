from mal_types import true, false, nil, Array, String
from printer import pr_str

def prn(*args):
    print(" ".join([pr_str(x) for x in args]))
    return nil()

def println(*args):
    print(" ".join([pr_str(x, print_readably=False) for x in args]))
    return nil()

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
    'pr-str': lambda *args: String(" ".join([pr_str(x, print_readably=True) for x in args])),
    'str': lambda *args: String(" ".join([pr_str(x, print_readably=False) for x in args])),
    'println': lambda *args: println(*args)
}


