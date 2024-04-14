import re

class atom(object):
    
    def __init__(self, x):
        self.reference = x

class Symbol:
    
    def __init__(self, name):
        self.name = name
        
    def __eq__(self, other):
        if isinstance(other, Symbol) and self.name == other.name:
            return True
        else:
            return False

class Function:
    
    def __init__(self, x, params, env, fn, is_macro = False):
        self.x = x
        self.params = params
        self.env = env
        self.fn = fn
        self.is_macro = is_macro
    
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
        
    def __eq__(self, other):
        if isinstance(other, Array) and self.type in ["list","vector"] and self.type == other.type and super().__eq__(other):
            return True
        elif isinstance(other, Array) and self.type == "hash-map" and self.type == other.type:
            ans = True
            for i in range(0, len(self), 2):
                if (self[i] not in other) or (self[i+1] != other[other.index(self[i])+1]):
                    ans = False
                    break
            
            if len(self) != len(other):
                ans = False
            
            return ans
        else:
            return False
        
    