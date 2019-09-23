import asyncio
from typing import Optional

import click
from my_ip.core import get_ip
from my_ip.settings import get_settings, default_config


def print_ip(path: Optional[str] = None) -> None:
    settings = get_settings(path)
    services = settings.service.values()
    loop = asyncio.get_event_loop()
    coro = get_ip(services)
    ip = loop.run_until_complete(coro)
    if ip is None:
        exit(1)
    print(ip)


@click.command()
@click.option(
    "--config",
    show_default=True,
    type=click.Path(exists=True),
    default=default_config(),
    help="path to config file",
)
def cli(config: str) -> None:
    print_ip(config)
