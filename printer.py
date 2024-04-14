import mal_types

def pr_str(mal_obj, print_readably = True):    
    if isinstance(mal_obj, int):
        return str(mal_obj)
    elif callable(mal_obj) or isinstance(mal_obj, mal_types.Function):
        return "#<function>"
    elif isinstance(mal_obj, mal_types.Symbol):
        return mal_obj.name
    elif isinstance(mal_obj, str):
        if print_readably:
            string_value = mal_obj.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            return '"' + string_value + '"'
        else:
            return  mal_obj
    elif isinstance(mal_obj, mal_types.Array):
        if mal_obj.type == "list":
            return "(" + " ".join([pr_str(x) for x in mal_obj]) + ")"
        elif mal_obj.type == "vector":
            return "[" + " ".join([pr_str(x) for x in mal_obj]) + "]"
        elif mal_obj.type == "hash-map":
            return "{" + " ".join([pr_str(x) for x in mal_obj]) + "}"
    elif mal_obj is None:
        return "nil"
    elif isinstance(mal_obj, mal_types.bool):
        if mal_obj.value:
            return "true"
        else:
            return "false"
    else:
        return str(mal_obj)