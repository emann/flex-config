from typing import Any, List, Tuple


def top_level_key_and_nested_subkey_dict(subkeys: List[str], value: Any) -> Tuple[str, Any]:
    top_level_key = subkeys[0]
    if len(subkeys) == 1:
        return top_level_key, value

    nested_dict = {subkeys[-1]: value}
    # Iterate subkeys in reverse order from the second to last subkey to the second subkey and nest the dict
    for subkey in subkeys[-2:0:-1]:
        nested_dict = {subkey: nested_dict}
    return top_level_key, nested_dict
