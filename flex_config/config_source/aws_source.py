from typing import Any, Dict, Generator, Tuple

import boto3

from .config_source import ConfigSource


class AWSSource(ConfigSource):
    """ A ConfigSource that loads values from environment variables """

    def __init__(self, path: str, **kwargs: Any) -> None:
        """
        :param path: The path in AWS SSM Param Store that config value should be read from
        :param kwargs: kwargs to be passed to boto3.client
        """
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
