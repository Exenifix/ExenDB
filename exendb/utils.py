"""
Copyright 2022-present Exenifix
Licensed under MIT License (http://www.opensource.org/licenses/mit), see LICENSE for details.
"""
from sqlite3 import Cursor
from sqlite3 import connect as sqlite_connect

from .enums import SQLType

DEFAULT = 'DEFAULT'


def _dict_factory(cursor: Cursor, row):
    d = {}
    for i, col in enumerate(cursor.description):
        d[col[0]] = row[i]
    return d


def connect(name: str, *args, row_factory=DEFAULT, **kwargs):
    """Creates a connection to the database"""

    con = sqlite_connect(name, *args, **kwargs)
    if row_factory == DEFAULT:
        con.row_factory = _dict_factory
    elif row_factory != None:
        con.row_factory = row_factory

    return con


def _sqltype_kwargs_to_str(kwargs: 'dict[str, SQLType]') -> str:
    s = ''
    for name, _type in kwargs.items():
        s += f'{name} {_type.value}, '

    s = s[:-2]
    return s


def _get_select_query(*values: str,
                      _from,
                      where: str = None,
                      order_by: str = None,
                      group_by: str = None,
                      limit: int = None):
    q = f'SELECT {", ".join(values)} FROM {_from} \
{_ein("WHERE", where)} \
{_ein("ORDER BY", order_by)} \
{_ein("GROUP BY", group_by)} \
{"LIMIT " + limit if limit is not None else ""}'

    return q


def _eif(value, condition: bool) -> str:
    return value if condition else ""


def _ein(base, value) -> str:
    return base + " " + value + " " if value is not None else ""
