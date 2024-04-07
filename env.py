import mal_types

class Env:
    
    def __init__(self, outer):
        self.outer = outer
        self.data = {}
    
    def set(self, key, val):
        self.data[key.name] = val
       
    def find(self, key):
        if key in self.data.keys():
            return self
        elif self.outer is not mal_types.nil:
            return self.outer.find(key)
        else:
            return None
            
    def get(self, key):
        env = self.find(key)
        if env is None:
            raise KeyError(f"Symbol {key} not found in environment")    
        return env.data[key]
    