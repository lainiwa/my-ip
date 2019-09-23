import os
from typing import Dict, Optional

import toml

from pydantic import UrlStr, BaseModel


class Service(BaseModel):
    addr: UrlStr
    attr: Optional[str]


class Settings(BaseModel):
    service: Dict[str, Service]


def default_config() -> str:
    xdg_config_home = os.getenv("$XDG_CONFIG_HOME", "~/.config")
    unexpanded_tilde_config = os.path.join(xdg_config_home, "my_ip.toml")
    return os.path.expanduser(unexpanded_tilde_config)


def get_settings(path: Optional[str]) -> Settings:
    if path is None:
        path = default_config()
    return Settings(**toml.load(path))
