import re
from mal_types import *

OTC = {"(":")", "[":"]", "{":"}"}

class Reader:
    
    def __init__(self, tokens, position=0):
        self.tokens = tokens
        self.position = position
    
    def next(self):
        self.position += 1
        return self.tokens[self.position - 1]
        
    def peek(self):
        return self.tokens[self.position]
    
    
def read_str(str_in):
    tokens = tokenize(str_in)
    r_obj = Reader(tokens)
    return read_form(r_obj)
    

def tokenize(str_in):
    return re.findall(
        '''[\s,]*(~@|[\[\]{}()'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}('"`,;)]*)''',
        str_in,)[:-1]

def read_form(r_obj):
    token = r_obj.peek()
    if token in ['(', '[', '{']:
        return read_list(r_obj)
    else:
        return read_atom(r_obj)
    

def read_list(r_obj):
    """
    This function will repeatedly call read_form with the Reader object until it encounters a ')' token 
    (if it reach EOF before reading a ')' then that is an error). It accumulates the results into a List type. 
    If your language does not have a sequential data type that can hold mal type values you may need to implement
    one (in types.qx). Note that read_list repeatedly calls read_form rather than read_atom. 
    This mutually recursive definition between read_list and read_form is what allows lists to contain lists.
    """
    out = []
    b = r_obj.next()
    while r_obj.peek() != OTC[b]:
        out.append(read_form(r_obj))
    _ = r_obj.next()
    return Array(out,b)

def read_atom(r_obj):
    """
    This function will look at the contents of the token and return the appropriate scalar (simple/single) data type value.
    Initially, you can just implement numbers (integers) and symbols. This will allow you to proceed through the next couple
    of steps before you will need to implement the other fundamental mal types: nil, true, false, and string. The remaining 
    scalar mal type, keyword does not need to be implemented until step A (but can be implemented at any point between this 
    step and that). BTW, symbols types are just an object that contains a single string name value (some languages have symbol 
    types already).
    """
    
    token = r_obj.next()
    
    if re.match('[0-9]+', token):
        return int(token)
    elif re.match('^"', token):
        if token[-1] != '"':
            raise ValueError("String missing closing quote")
        else:
            return String(token[1:-1])
    elif re.match('^:', token):
        return String(token)
    else:
        return Symbol(token)