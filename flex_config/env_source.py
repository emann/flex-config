import os
from typing import Any, Dict, Iterable, Tuple

from .config_source import ConfigSource
from .utils import insert_value_at_nested_key


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
        from flex_config import EnvSource, ConfigSchema, construct_config

        class MyConfigSchema(ConfigSchema):
            thing1: str
            thing2: int

        # Say you have APP_ENV="live" and APP_DATABASE.URL="my_database_url" as environment variables
        my_config = construct_config(config_schema=MyConfigSchema, sources=EnvSource("APP_"))
        assert my_config.env = "live"
        assert my_config.database.url = "my_database_url"
        ```

    """

    def __init__(self, prefix: str, separator: str = ".") -> None:
        self.prefix = prefix
        self.separator = separator

    def to_dict(self) -> Dict[str, Any]:
        """ Returns a generator for getting all key, value pairs """
        param_dict: Dict[str, Any] = {}
        for key, value in os.environ.items():
            if not key.startswith(self.prefix):
                continue
            key = key.replace(self.prefix, "")
            param_dict = insert_value_at_nested_key(
                dest_dict=param_dict, subkey_path=key.split(self.separator), value=value
            )
        return param_dict

    def items(self) -> Iterable[Tuple[str, Any]]:
        """ Returns a generator for getting all key, value pairs """
        return self.to_dict().items()
