"""Configuration file related functions.

This module defines appropriate pydantic models for config file. This lets the
script to validate the settings while parsing them.
"""

from typing import Dict, Optional

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
