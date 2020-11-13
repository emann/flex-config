__all__ = ["ConfigSchema", "ConfigSource", "AWSSource", "EnvSource", "YAMLSource"]
from typing import Any, Callable, Dict, Sequence, Type, TypeVar, Union

from pydantic import BaseModel as ConfigSchema

from .aws_source import AWSSource
from .config_source import ConfigSource
from .env_source import EnvSource
from .yaml_source import YAMLSource

_SourceTypes = Union[ConfigSource, Callable[[Dict[str, Any]], ConfigSource]]


def _merge_sources(dest: Dict[str, Any], source: ConfigSource) -> Dict[str, Any]:
    """Merge the values in the source into the destination dictionary"""
    for key, val in source.items():
        if isinstance(val, dict):
            if key in dest:
                dest[key] = _merge_sources(dest[key], val)
            else:
                dest[key] = val.copy()
        else:
            dest[key] = val
    return dest


def _compile_sources(sources: Union[Sequence[_SourceTypes], _SourceTypes]) -> Dict[str, Any]:
    if not isinstance(sources, Sequence):
        sources = [sources]

    compiled: Dict[str, Any] = {}
    for source in sources:
        if callable(source):
            source = source(compiled)  # Pass what we have parsed so far to the function
        compiled = _merge_sources(dest=compiled, source=source)
    return compiled


ConfigClass = TypeVar("ConfigClass")


def construct_config(
    config_schema: Type[ConfigClass], sources: Union[Sequence[_SourceTypes], _SourceTypes]
) -> ConfigClass:
    if not isinstance(config_schema, ConfigSchema):
        raise TypeError("Config schema supplied isn't a subclass of ConfigSchema (aka Pydantic's BaseModel)")
    compiled_config_dict = _compile_sources(sources=sources)
    return config_schema(**compiled_config_dict)
