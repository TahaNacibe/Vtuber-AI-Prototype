from data.expressions import expressions_index
from costume_types.expression import ExpressionItem

def get_emotes_keys_list() -> list[str]:
    return expressions_index.keys()

def get_emotes_keys_string() -> str:
    keys_list = expressions_index.keys()
    return ", ".join(keys_list)

def get_emote_by_key(key:str) -> ExpressionItem:
    if key in expressions_index:
        return expressions_index[key]
    else:
        raise KeyError(f"Emote '{key}' not found in expressions index.")
    
    