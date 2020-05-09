# Flex Config
[![triaxtec](https://circleci.com/gh/triaxtec/flex-config.svg?style=svg)](https://app.circleci.com/pipelines/github/triaxtec/flex-config?branch=master)
[![codecov](https://codecov.io/gh/triaxtec/flex-config/branch/master/graph/badge.svg?token=3utvPfZSLB)](https://codecov.io/gh/triaxtec/flex-config)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Generic badge](https://img.shields.io/badge/type_checked-mypy-informational.svg)](https://mypy.readthedocs.io/en/stable/introduction.html)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)


Configure your applications as easily as possible.

## Main Features
### Load config from wherever
1. Comes with built in support for loading from dicts, environment variables, YAML files, and AWS SSM Parameter Store.
2. Super easy to set up a custom source and load from anywhere.

### Path-like lookups for nested values
```python
from flex_config import FlexConfig

flex_config = FlexConfig()
flex_config["app/env"] = "local"
assert flex_config["app"]["env"] == "local"
assert flex_config["app/env"] == "local"
```

### Basic type inference
If the value FlexConfig gets is a string (like you get from SSM and Env), it will try to parse it to a few other types.
1. Strings that are digits become ints
1. Numbers with decimals `.` become floats
1. Strings contained with `{` and `}` will be parsed as JSON
1. Failing any of the above you just get your string back

## Installation
Basic install: `poetry install flex_config`
With all optional dependencies: `poetry install flex_config -E all`

For a full tutorial and API docs, check out the [hosted documentation]


[hosted documentation]: https://triaxtec.github.io/flex-config
