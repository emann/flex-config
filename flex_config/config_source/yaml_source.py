from pathlib import Path
from typing import Any, Iterable, Tuple

import yaml

from .config_source import ConfigSource


class YAMLSource(ConfigSource):
    """ A ConfigSource that loads values from environment variables """

    def __init__(self, path: Path) -> None:
        """
        :param path: Path to the YAML file to load config from
        """
        super().__init__()
        self.path = path

    def items(self) -> Iterable[Tuple[str, Any]]:
        """ Returns a generator for getting all path, value pairs """
        if not self.path.exists():
            return []

        with self.path.open() as config_yml_file:
            config_dict = yaml.safe_load(config_yml_file)
            return config_dict.items()
