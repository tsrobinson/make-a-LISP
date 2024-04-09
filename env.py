import mal_types
import core

class Env:
    
    def __init__(self, outer, binds, exprs):
        self.outer = outer
        self.data = {}
        
        for i, key in enumerate(binds):
            
            if key == "&":
                self.data[binds[i+1]] = mal_types.Array(exprs[i:], "(")
                break
            else:
                self.data[key] = exprs[i]
    
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
    