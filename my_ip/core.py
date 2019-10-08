"""Core functionality.

Asynchronous aiohttp requests to IP returning services.
"""

import functools
import itertools
from typing import Iterable, Optional

import asks
import trio
from my_ip.settings import Service


async def _aenumerate(asequence, start=0):
    """Asynchronously enumerate an async iterator from a given start value."""
    n = itertools.count(start)
    async for elem in asequence:
        yield next(n), elem


async def _race(*async_fns):
    """Return first `not None` result of a buch of asynchronous functions."""
    if not async_fns:
        raise ValueError("must pass at least one argument")

    send_channel, receive_channel = trio.open_memory_channel(0)

    async def jockey(async_fn):
        await send_channel.send(await async_fn())

    async with trio.open_nursery() as nursery:
        # Producer
        for async_fn in async_fns:
            nursery.start_soon(jockey, async_fn)
        # Receiver
        async for i, winner in _aenumerate(receive_channel, 1):
            # Return value if it is a "success" (i.e. not None)
            if winner is not None:
                nursery.cancel_scope.cancel()
                return winner
            # If the last value processed was not a "success", we return None.
            # We _must_ want to do that explicitly, as we don't want to hang
            # in an empty query forever.
            if i == len(async_fns):
                return None


async def fetch(session, url, attr=None):
    """Fetch and parse data from a single `url`."""
    try:
        response = await session.get(url)
        return response.text.strip() if attr is None else response.json()[attr]
    except Exception:
        return None


def get_ip(services: Iterable[Service]) -> Optional[str]:
    """Get first IP from multiple services.

    Parameters:
        services: an iterable of services that should be requested for IP.

    Returns:
        A string with IP if success; returns `None` on failure.

    """
    session = asks.Session(connections=20)
    funcs = [
        functools.partial(fetch, session, service.url, service.attr)
        for service in services
    ]
    ip = trio.run(_race, *funcs)
    return ip
