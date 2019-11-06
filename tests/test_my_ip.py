"""Tests for my_ip package."""

from click.testing import CliRunner

from my_ip import __version__
from my_ip.console import cli


def test_version() -> None:
    """Test for version."""
    assert __version__ == "0.2.0"


def test_cli_version():
    """Test `mip --version` output."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert result.output == "my_ip version: 0.2.0\n"
