"""Command line interface.

The module specifies the script's CLI.
"""

import os
import asyncio
import pkgutil
from typing import Any, Union

import toml

import click
from my_ip import __version__
from my_ip.core import get_ip
from my_ip.settings import Settings


def print_ip(settings: Settings) -> None:
    """Get current IP address and print it.

    Exit with non-zero code on failure.

    Parameters:
        path: Location of the script's configuration file.

    """
    services = settings.service.values()
    loop = asyncio.get_event_loop()
    coro = get_ip(services)
    ip = loop.run_until_complete(coro)
    if ip is None:
        exit(1)
    print(ip)


def print_version(
    ctx: click.core.Context,
    param: Union[click.core.Option, click.core.Parameter],
    value: Any,
) -> Any:
    """Print version click callback."""
    if not value or ctx.resilient_parsing:
        return
    click.echo(__package__ + " version: " + __version__)
    ctx.exit()


@click.command()
@click.option(
    "--version",
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help="print package version and exit",
)
@click.option(
    "--config",
    type=click.Path(
        exists=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        allow_dash=True,
    ),
    default=None,
    help="path to config file",
)
def cli(config: str) -> None:
    """Find out your internet IP address."""
    std_config_dir = click.get_app_dir(__package__)
    std_config_path = os.path.join(std_config_dir, "config.toml")

    if not os.path.isfile(std_config_path):
        click.echo("First run.")
        click.echo(f"Installing config to `{std_config_path}`... ", nl=False)

        os.makedirs(std_config_dir, exist_ok=True)

        with open(std_config_path, "w") as file:
            file.write(
                pkgutil.get_data(__package__, "data/config.toml").decode(
                    "utf-8"
                )
            )

        click.echo("Done!")

    if config is None:
        config = std_config_path

    with click.open_file(config, "r") as fil:
        print_ip(Settings(**toml.loads(fil.read())))


if __name__ == "__main__":
    cli()
