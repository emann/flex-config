import os
from typing import Any, Generator, Tuple

from .config_source import ConfigSource


class EnvSource(ConfigSource):
    """ A ConfigSource that loads values from environment variables """

    def __init__(self, prefix: str, separator: str = ".") -> None:
        """
        :param prefix: case insensitive prefix of all environment variables to load (e.g. SPOTR_)
        :param separator: The character used as a separator between path parts in the variable name, defaults to .
        """
        self.prefix = prefix
        self.separator = separator

    def items(self) -> Generator[Tuple[str, Any], None, None]:
        """ Returns a generator for getting all path, value pairs """
        for key, value in os.environ.items():
            if not key.startswith(self.prefix):
                continue
            key = key.replace(self.prefix, "").replace(self.separator, "/").lower()
            yield key, value
