# Flex Config
[![codecov](https://codecov.io/gh/triaxtec/flex-config/branch/master/graph/badge.svg?token=3utvPfZSLB)](https://codecov.io/gh/triaxtec/flex-config)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Generic badge](https://img.shields.io/badge/type_checked-mypy-informational.svg)](https://mypy.readthedocs.io/en/stable/introduction.html)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)


Configure your applications as easily as possible.

## Main Features
### Load config from wherever
- Comes with built in support for loading from dicts, environment variables, JSON/YAML/TOML files, and AWS SSM Parameter Store.
- Super easy to set up a custom source and load from anywhere.

### Type conversion, validation, and hints via [Pydantic]
```python
# "ConfigSchema" is pydantic's BaseModel renamed and re-exported for easier use 
from flex_config import ConfigSchema, construct_config

class Config(ConfigSchema):
    a_string: str
    an_int: int

# Raises ValidationError
my_bad_config = construct_config(Config, {"a_string": ["not", "a", "string"], "an_int": "seven"})

my_good_config = construct_config(Config, {"a_string": "my_string", "an_int": "7"})
assert isinstance(my_good_config.an_int, int)
```

### Dynamic loading of config values
```python
from pathlib import Path
from typing import Dict, Any

# "ConfigSchema" is pydantic's BaseModel renamed and re-exported for easier use 
from flex_config import ConfigSchema, construct_config, AWSSource, YAMLSource, EnvSource, ConfigSource

class Config(ConfigSchema):
    env: str
    my_thing: str

def get_ssm_params(config_so_far: Dict[str, Any]) -> ConfigSource:
    # env is set to live or dev via environment variables in the deployment environment
    env = config_so_far.get("env")
    if env == "local":  # Not a live deployment, my_thing is in a local yaml file
        return {}
    return AWSSource(f"my_app/{config_so_far['env']}")


my_config = construct_config(Config, [EnvSource("MY_APP_"), YAMLSource(Path("my_file.yaml")), get_ssm_params])
```

## Installation
Basic install: `poetry install flex_config`
With all optional dependencies (support for AWS SSM, YAML, and TOML): `poetry install flex_config -E all`

For a full tutorial and API docs, check out the [hosted documentation]

[Pydantic]: https://github.com/samuelcolvin/pydantic/
[hosted documentation]: https://triaxtec.github.io/flex-config
