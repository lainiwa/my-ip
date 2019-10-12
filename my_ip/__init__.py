"""Getting current global IP.

Asynchronously request multiple services and get current IP address.
"""
import os
import sys

from xdg import BaseDirectory
from loguru import logger
from importlib_metadata import version

if __package__ is None:
    __package__ = 'my_ip'
__version__ = version(__package__)

# Ensure directory for logs exists
# and calculate log file path
log_dir = BaseDirectory.save_data_path(__package__)
log_path = os.path.join(log_dir, "debug.log")


# Remove default logger handler and substitute it with two other handlers:
#   * a less verbose - for CLI output
#   * and a more verbose - for logging into a file
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add(log_path, level="DEBUG", backtrace=True, diagnose=True)
