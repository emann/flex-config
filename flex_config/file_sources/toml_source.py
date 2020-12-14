from typing import Any, Dict, TextIO, cast

from .file_source import FileSource


class TOMLSource(FileSource):
    """
    A ConfigSource that loads values from a TOML file.

    Warning:
        In order to use this source you must have [toml](https://github.com/uiri/toml) installed either
        directly or by including the "toml" extra when installing this package
        (e.g. `poetry install flex-config -E toml`).

    Args:
        path (pathlib.Path): a [pathlib.Path](https://docs.python.org/3/library/pathlib.html#basic-use) to a TOML file
            to load.
        path_must_exist (bool): if true, the constructor will raise a RuntimeError if the provided path doesn't exist.

    Example:
        ```python
        from pathlib import Path
        from flex_config import TOMLSource, ConfigSchema, construct_config

        class MyConfigSchema(ConfigSchema):
            thing1: str
            thing2: int

        my_toml_file = Path("path/to/my.toml")
        my_config = construct_config(config_schema=MyConfigSchema, sources=TOMLSource(my_toml_file))
        ```

    """

    def _load_file(self, file: TextIO) -> Dict[str, Any]:
        """ Loads and parses the TOML file """
        import toml

        config_dict = toml.load(file)
        return cast(Dict[str, Any], config_dict)
