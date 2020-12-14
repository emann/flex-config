from typing import Any, Dict, TextIO

from .file_source import FileSource


class JSONSource(FileSource):
    """
    A ConfigSource that loads values from a JSON file.

    Args:
        path (pathlib.Path): a [pathlib.Path](https://docs.python.org/3/library/pathlib.html#basic-use) to a json file
            to load.
        path_must_exist (bool): if true, the constructor will raise a RuntimeError if the provided path doesn't exist.

    Example:
        ```python
        from pathlib import Path
        from flex_config import JSONSource, ConfigSchema, construct_config

        class MyConfigSchema(ConfigSchema):
            thing1: str
            thing2: int

        my_json_file = Path("path/to/my.json")
        my_config = construct_config(config_schema=MyConfigSchema, sources=JSONSource(my_json_file))
        ```
    """

    def _load_file(self, file: TextIO) -> Dict[str, Any]:
        """ Loads and parses the json file """
        import json

        config_dict = json.load(file)
        return config_dict
