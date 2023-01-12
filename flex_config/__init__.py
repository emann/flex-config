__all__ = ["ConfigSchema", "ConfigSource", "AWSSource", "EnvSource", "YAMLSource", "TOMLSource", "JSONSource"]
from typing import Any, Callable, Dict, Iterable, Sequence, Type, TypeVar, Union, cast

from pydantic import BaseModel as ConfigSchema

from .aws_source import AWSSource
from .config_source import ConfigSource
from .env_source import EnvSource
from .file_sources import JSONSource, TOMLSource, YAMLSource

_SourceTypes = Union[ConfigSource, Callable[[Dict[str, Any]], Union[ConfigSource, Sequence[ConfigSource]]]]


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
    """Compiles the sources passed into a single dictionary"""
    if not isinstance(sources, Sequence):
        sources = [sources]

    compiled: Dict[str, Any] = {}
    for source in sources:
        if callable(source):
            # This is a function that returns an iterable of sources
            source_func_return_val = source(compiled)  # Pass what we have parsed so far to the function

            if isinstance(source_func_return_val, Sequence):
                # Source generator returned an iterable of sources, go through and merge each one
                for generated_source in source_func_return_val:
                    compiled = _merge_sources(dest=compiled, source=generated_source)
            else:
                # Source generator returned a single source
                compiled = _merge_sources(dest=compiled, source=source_func_return_val)
        else:
            compiled = _merge_sources(dest=compiled, source=source)

    return compiled


ConfigClass = TypeVar("ConfigClass")


def construct_config(
    config_schema: Type[ConfigClass], sources: Union[Sequence[_SourceTypes], _SourceTypes]
) -> ConfigClass:
    """Loads values from the sources passed in (in order) and creates an instance of the config schema specified.

    Args:
        config_schema: a subclass of ConfigSchema (or Pydantic's BaseModel) to validate config values with
        sources: A list of ConfigSources to be loaded and merged in the order they were passed in

    Returns:
        An instance of the config schema passed in containing values loaded (in order) from the sources passed in

    Raises:
        TypeError: If config_schema passed in is not a subclass of ConfigSchema (which is just a renamed and re-exported
            [pydantic.BaseModel](https://pydantic-docs.helpmanual.io/usage/models/#basic-model-usage) which you could
            subclass instead if you already have it imported)
        ValidationError: If there are issues validating the compiled config values e.g. missing values or values that
            couldn't be converted to their specified type
    """
    if not issubclass(config_schema, ConfigSchema):
        raise TypeError("Config schema supplied isn't a subclass of ConfigSchema (aka Pydantic's BaseModel)")
    compiled_config_dict = _compile_sources(sources=sources)
    return cast(ConfigClass, config_schema(**compiled_config_dict))
