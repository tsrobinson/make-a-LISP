from mal_types import Symbol
def pr_str(mal_obj):
    
    if isinstance(mal_obj, int):
        return(str(mal_obj))
    elif isinstance(mal_obj, Symbol):
        return(mal_obj.name)
    elif isinstance(mal_obj, list):
        return("(" + " ".join([pr_str(x) for x in mal_obj]) + ")")
        
    