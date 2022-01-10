"""
Copyright 2022-present Exenifix
Licensed under MIT License (http://www.opensource.org/licenses/mit), see LICENSE for details.
"""
from enum import Enum


def _to_sql_format(value):
    if type(value) in (int, float):
        return str(value)
    elif type(value) == str:
        return f'"{value}"'
    elif type(value) == bytes:
        return str(value.decode())
    elif type(value) == bool:
        return str(value).lower()
    elif value == None:
        return 'NULL'


class FetchMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class SQLType(Enum):
    TEXT = 'TEXT'
    INT = 'INTEGER'
    BOOL = 'BOOL'
    BOOLEAN = 'BOOL'
    INTEGER = 'INT'
    REAL = 'REAL'
    NULL = 'NULL'
    FLOAT = 'REAL'
    BLOB = 'BLOB'

    @staticmethod
    def _with_modifier(_type, modifier):
        return ConstraintType(_type.value + ' ' + modifier)

    @staticmethod
    def PRIMARY_KEY(_type):
        """Returns type with PRIMARY KEY modifier"""
        return SQLType._with_modifier(_type, 'PRIMARY KEY')

    @staticmethod
    def NOT_NULL(_type):
        """Returns type with NOT NULL modifier"""
        return SQLType._with_modifier(_type, 'NOT NULL')

    @staticmethod
    def UNIQUE(_type):
        """Returns type with UNIQUE modifier"""
        return SQLType._with_modifier(_type, 'UNIQUE')

    @staticmethod
    def DEFAULT(_type, default_value):
        """Return type with DEAFULT `default_value` modifier"""
        return SQLType._with_modifier(_type, 'DEFAULT ' + _to_sql_format(default_value))


class ConstraintType():
    def __init__(self, value):
        self.value = value
