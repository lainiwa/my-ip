import asyncio
from typing import Tuple, Iterable, Optional

import aiohttp
from my_ip.settings import Service


async def try_service(
    session: aiohttp.ClientSession, url: str, attr: Optional[str] = None
) -> Tuple[str, str]:
    async with session.get(url) as response:
        if attr is None:
            text = await response.text()
            return url, text.strip()
        else:
            json = await response.json()
            return url, json[attr]


async def get_ip(services: Iterable[Service]) -> Optional[str]:
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
