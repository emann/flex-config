from pathlib import Path
from typing import Dict, Optional, Any

from flex_config import AWSSource, EnvSource, FlexConfig, YAMLSource

_app_config: Optional[FlexConfig] = None
yaml_path = Path.cwd() / "config.yml"


default_config = {
    "env": "local",
}


def get_config(override: Dict[str, Any] = None) -> FlexConfig:
    """ Get the app config for this  """
    global _app_config

    if _app_config:
        return _app_config

    if not override:
        override = {}

    _app_config = FlexConfig()
    _app_config.load_sources([
        default_config,
        EnvSource("APP_"),
        YAMLSource(yaml_path),
        override,
    ])

    env = _app_config["env"]
    if env != "local":
        _app_config.load_sources(AWSSource(f"app/{env}"))

    return _app_config
