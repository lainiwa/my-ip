"""Configuration file related functions.

This module defines appropriate pydantic models for config file. This lets the
script to validate the settings while parsing them.

The module also defines a function specifying the right place to search for
the config, respecting XDG Base Directory Specification.
"""

import os
from typing import Dict, Optional

import toml

from pydantic import UrlStr, BaseModel


class Service(BaseModel):
    """Model of single IP service.

    Attributes:
        addr: URL of the service.
        attr: what attribute to extract as IP, if the service returns JSON.

    """

    addr: UrlStr
    attr: Optional[str]


class Settings(BaseModel):
    """Model of whole configuration file.

    Attributes:
        service: top-level key, mapping a dictionary of available services

    """

    service: Dict[str, Service]


def default_config() -> str:
    """Config default path.

    Returns:
        Expected path of the configuration file.

    """
    xdg_config_home = os.getenv("$XDG_CONFIG_HOME", "~/.config")
    unexpanded_tilde_config = os.path.join(xdg_config_home, "my_ip.toml")
    return os.path.expanduser(unexpanded_tilde_config)


def get_settings(path: Optional[str]) -> Settings:
    """Parse and validate configuration file.

    Parameters:
        path: configuration file location.

    Returns:
        Model of the configuration file.

    """
    if path is None:
        path = default_config()
    return Settings(**toml.load(path))
