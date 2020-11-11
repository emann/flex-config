from typing import Any, Dict, List


def insert_value_at_nested_key(dest_dict: Dict[str, Any], subkey_path: List[str], value: Any) -> Dict[str, Any]:
    subkey_path = [s.lower() for s in subkey_path]
    nested_dict = dest_dict
    for subkey in subkey_path[:-1]:
        nested_dict = nested_dict.setdefault(subkey, {})
    nested_dict[subkey_path[-1]] = value
    return dest_dict
