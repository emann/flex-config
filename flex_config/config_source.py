from typing import Any, Iterable, Protocol, Tuple


class ConfigSource(Protocol):
    """The protocol required to be used as a source of values in a FlexConfig

    This is very much intended to support builtin `dict` as a source.
    """

    def items(self) -> Iterable[Tuple[str, Any]]:
        """ A function to getting key, value pairs to store in the FlexConfig """
