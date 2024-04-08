from mal_types import true, false
from printer import pr_str

ns = {
    '+': lambda a,b: a+b,
    '-': lambda a,b: a-b,
    '*': lambda a,b: a*b,
    '/': lambda a,b: int(a/b),
    'prn': lambda *args: prn(args[0]),
    'list': lambda *args: list(*args),
    'list?': lambda *args:true() if isinstance(args[0], list) else false(),
    'empty?': lambda *args: true() if args[0] == [] else false(),
    'count': lambda *args: len(args[0]),
    '=': lambda a,b: true() if a==b else false(),
    '<': lambda a,b: true() if a<b else false(),
    '<=': lambda a,b: true() if a<=b else false(),
    '>': lambda a,b: true() if a>b else false(),
    '>=': lambda a,b: true() if a>=b else false(),
}


def prn(a):
    pr_str(a, print_readably = True)
    return mal_types.nil()