import json
from typing import Any, Dict, Iterable, Tuple

from .config_source import ConfigSource
from .utils import insert_value_at_nested_key


class AWSSource(ConfigSource):
    """
    A ConfigSource that loads values recursively from an AWS SSM path.

    Warning:
        In order to use this source you must have
        [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
        installed either directly or by including the "aws" extra when installing this package
        (e.g. `poetry install flex-config -E aws`).

    Args:
        path (str): a prefix in AWS SSM to read from.

    Info:
        You can pass any keyword arguments to this class that you would to boto3 directly (e.g. secret key).

    Example:
        ```python
        from flex_config import AWSSource, FlexConfig, construct_config

        class MyConfigSchema(ConfigSchema):
            thing1: str
            thing2: int

        my_config = construct_config(config_schema=MyConfigSchema, sources=AWSSource(f"my_app/dev"))
        ```

    """

    def __init__(self, path: str, **kwargs: Any) -> None:
        import boto3

        self.ssm = boto3.client("ssm", "us-east-1", **kwargs)
        self.path = path

    def to_dict(self) -> Dict[str, Any]:
        """ Returns a generator for getting all path, value pairs """
        kwargs: Dict[str, Any] = {}
        param_dict: Dict[str, Any] = {}
        while True:
            result = self.ssm.get_parameters_by_path(
                Path=f"/{self.path}/", Recursive=True, WithDecryption=True, **kwargs
            )

            for param in result["Parameters"]:
                path = param["Name"].replace(f"/{self.path}/", "")  # Don't repeat SSM path in key

                value = param["Value"]
                if isinstance(value, str) and (value.startswith("{") or value.startswith("[")):
                    try:
                        value = json.loads(value)
                    except json.JSONDecodeError:
                        pass

                param_dict = insert_value_at_nested_key(dest_dict=param_dict, subkey_path=path.split("/"), value=value)

            kwargs["NextToken"] = result.get("NextToken")
            if kwargs["NextToken"] is None:  # That's the last of the values
                break
        return param_dict

    def items(self) -> Iterable[Tuple[str, Any]]:
        """ Returns a generator for getting all path, value pairs """
        return self.to_dict().items()
