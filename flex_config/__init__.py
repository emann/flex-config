import json
from typing import Any, Dict, Iterable, Optional, Sequence, Set, Union

from .aws_source import AWSSource
from .config_source import ConfigSource
from .env_source import EnvSource
from .yaml_source import YAMLSource


class FlexConfig(Dict[str, Any]):
    """ Holds config values which can be loaded from many sources """

    def __init__(self, required: Set[str] = None) -> None:
        super().__init__()
        self.required: Optional[Set[str]] = required

    def load_sources(self, config_sources: Union[Sequence[ConfigSource], ConfigSource]) -> None:
        """
        Load the data from a [ConfigSource][flex_config.config_source.ConfigSource] or list thereof

        Args:
            config_sources: A Single or ConfigSource or Iterable of ConfigSources.
        
        """

        if not isinstance(config_sources, Sequence):
            config_sources = [config_sources]

        for source in config_sources:
            for (path, value) in source.items():
                self[path] = value

    def validate(self) -> None:
        """
        Verify that all required attributes are set

        Raises:
            KeyError: If any required attribute is missing
        """
        if self.required is None:
            return

        for attr in self.required:
            # noinspection PyStatementEffect
            self[attr]

    @staticmethod
    def flatten_dict(d: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes a dict with potentially nested values and returns a flat dict

        Returns:
            Flattened dictionary
        """

        keys = list(d.keys())  # can't be an iterator because we're modifying in this loop
        for key in keys:
            if isinstance(d[key], dict):  # This is a dict within the top level dict
                d[key] = FlexConfig.flatten_dict(d[key])  # First flatten the internal dict
                for inner_key, inner_value in d[key].items():  # Now pull all of its keys into the top level dict
                    d[f"{key}/{inner_key}"] = inner_value
                del d[key]
        return d

    @staticmethod
    def _value_from_string(value: str) -> Any:
        if value.isdigit():
            return int(value)
        elif value.startswith("{") and value.endswith("}"):
            return json.loads(value)
        elif "." in value:
            # noinspection PyBroadException
            # Test to see if this value is a float
            try:
                return float(value)
            except:
                pass
        return value

    def __getitem__(self, item: str) -> Any:
        path_parts = item.split("/")
        current = super().__getitem__(path_parts[0])

        for part in path_parts[1:]:
            if isinstance(current, dict):
                current = current[part]
        return current

    def get(self, item: str, default: Any = None) -> Any:
        """ Get a value if it exists, if not return None """
        try:
            return self[item]
        except KeyError:
            return default

    def __setitem__(self, key: str, value: Any) -> None:
        """ Create or update the value at specified /-delimited path.  Creates a dict structure for nested path parts"""
        path_parts = key.split("/")

        if isinstance(value, str):
            value = FlexConfig._value_from_string(value)
        if isinstance(value, dict):
            # Could be updating multiple items, flatten and set them one at a time
            for inner_key, inner_value in FlexConfig.flatten_dict(value).items():
                self[f"{key}/{inner_key}"] = inner_value
            return

        target = self
        for part in path_parts[:-1]:
            target = target.setdefault(part, {})

        if target is self:  # Make sure we don't recursively call this fn again
            super().__setitem__(path_parts[-1], value)
        else:
            target[path_parts[-1]] = value


__all__ = ["FlexConfig", "ConfigSource", "AWSSource", "EnvSource", "YAMLSource"]
