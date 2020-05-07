from pathlib import Path
from typing import Any, Iterable, Tuple

from .config_source import ConfigSource


class YAMLSource(ConfigSource):
    """
    A ConfigSource that loads values from a YAML file.

    Warning:
        In order to use this source you must have [pyyaml](https://pyyaml.org/wiki/PyYAMLDocumentation) installed either
        directly or by including the "yaml" extra when installing this package
        (e.g. `poetry install flex-config -E yaml`).

    Args:
        path (pathlib.Path): a [pathlib.Path](https://docs.python.org/3/library/pathlib.html#basic-use) to a YAML file
            to load.

    Example:
        ```python
        from pathlib import Path
        from flex_config import FlexConfig, YAMLSource

        my_yaml_file = Path("path/to/my.yaml")
        yaml_source = YAMLSource(my_yaml_file)
        my_config = FlexConfig()
        my_config.load_sources(yaml_source)
        ```

    """

    def __init__(self, path: Path) -> None:
        super().__init__()
        self.path = path

    def items(self) -> Iterable[Tuple[str, Any]]:
        """ Returns a generator for getting all path, value pairs """
        import yaml

        if not self.path.exists():
            return []

        with self.path.open() as config_yml_file:
            config_dict = yaml.safe_load(config_yml_file)
            return config_dict.items()
