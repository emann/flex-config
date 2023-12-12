from pathlib import Path
from typing import Any, Dict, Optional

from flex_config import AWSSource, ConfigSchema, ConfigSource, EnvSource, YAMLSource, construct_config


class DataBaseConfig(ConfigSchema):
    url: str
    username: str
    password: str


class SentryConfig(ConfigSchema):
    url: str
    traces_sample_rate: float = 0.1


class Config(ConfigSchema):
    env: str
    special_number: int
    database: DataBaseConfig
    sentry: SentryConfig


def get_ssm_params(config_so_far: Dict[str, Any]) -> ConfigSource:
    env = config_so_far.get("env")
    if env == "local":
        return {}
    return AWSSource(f"my_app/{env}")


default_config = {
    "env": "local",
}


_app_config: Optional[Config] = None
yaml_path = Path.cwd() / "config.yml"


def get_config(override: Dict[str, Any] = None) -> Config:
    """Get the app config for this app"""
    global _app_config

    if _app_config:
        return _app_config

    if not override:
        override = {}

    _app_config = construct_config(
        config_schema=Config,
        sources=[
            default_config,
            EnvSource("CAT_"),
            YAMLSource(yaml_path),
            get_ssm_params,
            override,
        ],
    )

    return _app_config
