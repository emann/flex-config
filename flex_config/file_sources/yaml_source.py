from typing import Any, Dict, TextIO

from .file_source import FileSource


class YAMLSource(FileSource):
    """
    A ConfigSource that loads values from a YAML file.

    Warning:
        In order to use this source you must have [pyyaml](https://pyyaml.org/wiki/PyYAMLDocumentation) installed either
        directly or by including the "yaml" extra when installing this package
        (e.g. `poetry install flex-config -E yaml`).

    Args:
        path (pathlib.Path): a [pathlib.Path](https://docs.python.org/3/library/pathlib.html#basic-use) to a YAML file
            to load.
        path_must_exist (bool): if true, the constructor will raise a RuntimeError if the provided path doesn't exist.

    Example:
        ```python
        from pathlib import Path
        from flex_config import YAMLSource, ConfigSchema, construct_config

        class MyConfigSchema(ConfigSchema):
            thing1: str
            thing2: int

        my_yaml_file = Path("path/to/my.yaml")
        my_config = construct_config(config_schema=MyConfigSchema, sources=YAMLSource(my_yaml_file))
        ```
    """

    def _load_file(self, file: TextIO) -> Dict[str, Any]:
        """ Loads and parses the YAML file """
        import yaml

        config_dict = yaml.safe_load(file)
        return config_dict
