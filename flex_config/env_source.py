import os
from typing import Any, Generator, Tuple

from .config_source import ConfigSource


class EnvSource(ConfigSource):
    """
    A ConfigSource that loads values from environment variables.

    Args:
        prefix (str): a prefix for all environment variables that should be loaded (e.g. "APP_"). Only vars which begin
            with the prefix will be loaded.
        separator (str): a string that will separate nested values. Defaults to `.`

    Note:
        All keys will be converted to lower case with the prefix stripped.

    Example:
        ```python
        from flex_config import EnvSource, FlexConfig

        # Say you have APP_ENV and APP_DATABASE.URL as environment variables
        env_source = EnvSource("APP_")
        my_config = FlexConfig()
        my_config.load_sources(env_source)
        assert "env" in my_config
        assert "database" in my_config
        assert "url" in my_config["database"]
        ```

    """

    def __init__(self, prefix: str, separator: str = ".") -> None:
        self.prefix = prefix
        self.separator = separator

    def items(self) -> Generator[Tuple[str, Any], None, None]:
        """ Returns a generator for getting all path, value pairs """
        for key, value in os.environ.items():
            if not key.startswith(self.prefix):
                continue
            key = key.replace(self.prefix, "").replace(self.separator, "/").lower()
            yield key, value
