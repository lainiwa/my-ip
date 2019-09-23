"""Core functionality.

Asynchronous aiohttp requests to IP returning services.
"""

import asyncio
from typing import Tuple, Iterable, Optional

import aiohttp
from my_ip.settings import Service


async def try_service(
    session: aiohttp.ClientSession, url: str, attr: Optional[str] = None
) -> Tuple[str, str]:
    """Send request to a single service.

    Parameters:
        session: aiohttp session object, so a function could reuse it.
        url: addressee of the request
        attr: if service returns JSON in response, use this attribute to
            extract the IP; `None` otherwise.

    Returns:
        A tuple with the service's `url` and the IP extracted from response.

    """
    async with session.get(url) as response:
        if attr is None:
            text = await response.text()
            return url, text.strip()
        else:
            json = await response.json()
            return url, json[attr]


async def get_ip(services: Iterable[Service]) -> Optional[str]:
    """Get first IP from multiple services.

    Parameters:
        services: an iterable of services that should be requested for IP.

    Returns:
        A string with IP if success; returns `None` on failure.

    """
    async with aiohttp.ClientSession() as session:
        futures = [
            try_service(session, service.addr, service.attr)
            for service in services
        ]

        for future in asyncio.as_completed(futures):
            try:
                url, ip = await future
                return ip
            except Exception:
                pass

        return None
