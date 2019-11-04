"""Configuration file related functions.

This module defines appropriate pydantic models for config file. This lets the
script to validate the settings while parsing them.
"""

from typing import Dict, Optional

from pydantic import HttpUrl, BaseModel


class Service(BaseModel):
    """Model of single IP service.

    Attributes:
        url: URL of the service.
        attr: what attribute to extract as IP, if the service returns JSON.

    """

    url: HttpUrl
    attr: Optional[str]


class Session(BaseModel):
    """Model of HTTP session parameters.

    Attributes:
        connections: how many connections in parallel we can open.
        headers: HTTP headers

    """

    connections: int
    headers: Dict[str, str]


class Settings(BaseModel):
    """Model of whole configuration file.

    Attributes:
        session: parameters of the HTTP session for requests
        service: top-level key, mapping a dictionary of available services

    """

    session: Session
    service: Dict[str, Service]
