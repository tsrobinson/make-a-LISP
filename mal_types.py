import re

class atom(object):
    
    def __init__(self, x):
        self.reference = x

class Symbol:
    
    def __init__(self, name):
        self.name = name

class Function:
    
    def __init__(self, x, params, env, fn):
        self.x = x
        self.params = params
        self.env = env
        self.fn = fn
    
class bool:
    
    def __init__(self):
        pass    
    
class true(bool):
    
    def __init__(self):
        super().__init__()
        self.value = True
    
class false(bool):
    
    def __init__(self):
        super().__init__()
        self.value = False

class Array(list):
    
    def __init__(self, x, bracket):
        super().__init__(x)
                
        if bracket == "(":
            self.type = "list"
        elif bracket == "[":
            self.type = "vector"
        elif bracket == "{":
            self.type = "hash-map"
        else:
            raise ValueError("Invalid array type")