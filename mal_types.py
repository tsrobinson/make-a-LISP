import re

class Symbol:
    
    def __init__(self, name):
        self.name = name

class nil:
    
    def __init__(self):
        pass
    
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
    
class String:
    """
    When a string is read, the following transformations are applied: 
    a backslash followed by a doublequote is translated into a plain doublequote character, 
    a backslash followed by "n" is translated into a newline, 
    and a backslash followed by another backslash is translated into a single backslash.
    """    
    def __init__(self, value):
        
        value.replace('\\"', '"')
        value.replace('\\n', '\n')
        value.replace('\\\\', '\\')
        self.value = value
