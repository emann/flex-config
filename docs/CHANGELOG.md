# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 2.0.0 - unreleased

### Breaking Chnages
- Complete rework of how FlexConfig works. [Pydantic](https://pydantic-docs.helpmanual.io/) schemas are now used to define
    the shape and data in a config, but loading values from sources works the same way. Config values are now retrieved
    via dot notation (`my_config.section.value`) instead of the "slash" notation in 1.x (`my_config["section/value"]`).
    See documentation for more info.
    
### Additions:
- Thanks to pydantic's built in data validation/conversion, the structure of the config and the types of it values are
    now strictly enforced so you can be sure that if your program starts without any validation errors the config is
    correctly built and all data types match what they are expected to be.

## 1.0.0 - 2020-05-09
Initial release
