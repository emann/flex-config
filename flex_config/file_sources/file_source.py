from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Iterable, TextIO, Tuple

from flex_config.config_source import ConfigSource


class FileSource(ConfigSource, ABC):
    """
    A ConfigSource that loads values from a file. Should not be used directly - use one its subclasses for the supported
        file types.

    Args:
        path (pathlib.Path): a [pathlib.Path](https://docs.python.org/3/library/pathlib.html#basic-use) to a file
            (of a supported type) to load.
        path_must_exist (bool): Enforce that the passed path must exist. If not, default to empty source.

    Raises:
        FileExistsError: If path_must_exist is true but the path does not exist
    """

    def __init__(self, path: Path, path_must_exist: bool = False) -> None:
        super().__init__()
        if path_must_exist and not path.exists():
            raise FileNotFoundError(f'Config file at "{path}" does not exist!')
        self.path = path

    @abstractmethod
    def _load_file(self, file: TextIO) -> Dict[str, Any]:
        """ Loads/parses the file """
        raise NotImplementedError  # pragma: no cover

    def items(self) -> Iterable[Tuple[str, Any]]:
        """ Returns a generator for getting all path, value pairs """
        if not self.path.exists():
            return []

        with self.path.open() as config_file:
            config_dict = self._load_file(config_file)

        if isinstance(config_dict, list):
            raise ValueError(f"{self.path} contains a list at the top level instead of a dict")

        return config_dict.items()
