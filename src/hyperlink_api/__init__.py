"""An API for interfacing with hyperlink databases"""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("hyperlink-api")
except PackageNotFoundError:
    __version__ = "uninstalled"

__author__ = "Hyperlink"
__email__ = "barnish.harry@gmail.com"

from .v1.checkers import *

from .v1.test import *

from ._application import app
from .cli import cli
