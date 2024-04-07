import mal_types

def pr_str(mal_obj):    
    if isinstance(mal_obj, int):
        return(str(mal_obj))
    elif isinstance(mal_obj, mal_types.Symbol):
        return(mal_obj.name)
    elif isinstance(mal_obj, mal_types.String):
        return('"' + mal_obj.value + '"')
    elif isinstance(mal_obj, mal_types.Array):
        if mal_obj.type == "list":
            return("(" + " ".join([pr_str(x) for x in mal_obj]) + ")")
        elif mal_obj.type == "vector":
            return("[" + " ".join([pr_str(x) for x in mal_obj]) + "]")
        elif mal_obj.type == "hash-map":
            return("{" + " ".join([pr_str(x) for x in mal_obj]) + "}")