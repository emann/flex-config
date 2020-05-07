from typing import Any, Dict, Generator, Tuple

from .config_source import ConfigSource


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
        from flex_config import AWSSource, FlexConfig

        aws_source = AWSSource(f"my_app/dev")
        my_config = FlexConfig()
        my_config.load_sources(aws_source)
        ```

    """

    def __init__(self, path: str, **kwargs: Any) -> None:
        import boto3

        self.ssm = boto3.client("ssm", "us-east-1", **kwargs)
        self.path = path

    def items(self) -> Generator[Tuple[str, Any], None, None]:
        """ Returns a generator for getting all path, value pairs """
        kwargs: Dict[str, Any] = {}
        while True:
            result = self.ssm.get_parameters_by_path(
                Path=f"/{self.path}/", Recursive=True, WithDecryption=True, **kwargs
            )

            for param in result["Parameters"]:
                key = param["Name"].replace(f"/{self.path}/", "")  # Don't repeat SSM path in key
                yield key, param["Value"]

            kwargs["NextToken"] = result.get("NextToken")
            if kwargs["NextToken"] is None:  # That's the last of the values
                break
