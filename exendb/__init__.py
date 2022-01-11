"""
ExenDB
~~~~~~~~~~~~~~~

A simple library that covers sqlite3's basic functionality.

Copyright 2022-present Exenifix
Licensed under MIT License (http://www.opensource.org/licenses/mit), see LICENSE for details."""

__title__ = "exendb"
__author__ = "Exenifix"
__license__ = "MIT"
__copyright__ = "2022-present Exenifix"
__version__ = "0.0.2"

from .datamodels import *

__all__ = ['Database', 'Table', 'SQLType']
