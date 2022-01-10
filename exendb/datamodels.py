"""
Copyright 2022-present Exenifix
Licensed under MIT License (http://www.opensource.org/licenses/mit), see LICENSE for details.
"""

from typing import Union

from .enums import FetchMode, SQLType, _to_sql_format
from .exceptions import TableNotFound
from .utils import (DEFAULT, _eif, _ein, _get_select_query,
                    _sqltype_kwargs_to_str, connect)


class Database():
    """Class representing a database.
    
    Attributes
    ==========
    name: `str`
        Name of the database (without file extension).
    file_name: `str`
        Filename of the database we connect to.
    tables: `property, str`
        List of tables that belong to this database.
        
    Methods
    ==========
    `get_table(name: str)` -> `Table`
        Returns `Table` object if found in database's tables list.

    `create_table(name: str, **columns: SQLType)` -> `Table`
        Creates a new table and returns `Table` object.

    `delete_table(name: str)`
        Removes an existing table from the database.

    `select(*args, **kwargs)` -> `Union[dict, list]`
        Performs a `SELECT` query to the database.
    """
    def __init__(self, name, file_extension='db', **connection_settings):
        """Constructor for the `Database` class.
        
        Parameters
        ===========
        name: `str`
            Name of the database without file extension.
        file_extension: `str = 'db'`
            File extension of the database. Defaults to `db`.
        connection_settings
            Any keyword arguments that are required to be provided into `sqlite3.connect()`"""
        self.name = name
        self.file_name = self.name + '.' + file_extension
        self._connection_settings = connection_settings

    def _connect(self, _row_factory=DEFAULT):
        return connect(self.file_name, row_factory=_row_factory, **self._connection_settings)

    def _execute(self, query, fetch_mode: FetchMode = FetchMode.ONE, _row_factory=DEFAULT) -> Union[dict, list]:
        con = self._connect(_row_factory)
        cur = con.cursor()
        result = cur.execute(query)
        con.commit()
        final_result = None

        if fetch_mode == FetchMode.NONE:
            return
        elif fetch_mode == FetchMode.ONE:
            final_result = result.fetchone()
        elif fetch_mode == FetchMode.ALL:
            final_result = result.fetchall()

        return final_result

    @property
    def tables(self):
        """List of tables that belong to this database."""
        return [Table(self, name) for name in [i["name"] for i in self._execute('SELECT name FROM sqlite_master WHERE type="table"', FetchMode.ALL)]]

    def get_table(self, name: str):
        """
        Returns
        ==========
        `Table` object if found in database's tables list.

        Parameters
        ==========

        name: `str`
            Name of the table you would like to get.
        """
        for table in self.tables:
            if table.name == name:
                return table

        raise TableNotFound(name)

    def create_table(
            self,
            _name: str, *,
            if_not_exists: bool = True,
            without_rowid: bool = False,
            **columns: SQLType):
        """Creates a new table

        Returns
        ==========
        A new `Table` created.

        Parameters
        ==========
        name: `str`
            Name of the table you would like to create.
        if_not_exists: `bool` = True
            Prevents function from raising an exception in case table with provided `name` already exists when set to `True`.
        columns: `**kwargs`
            What columns to add to the table, name of kwarg is column name and value of kwarg is column type (`SQLType`).

        Example
        ==========
        `database.create_table("users", id=SQLType.INT, name=SQLType.TEXT)`
        will create a table with name "users" and columns "id" of type INT and "name" of type TEXT"""

        self._execute(
            f'CREATE TABLE {_eif("IF NOT EXISTS ", if_not_exists)}{_name} ({_sqltype_kwargs_to_str(columns)}) {_eif("WITHOUT ROWID", without_rowid)}')

        return self.get_table(_name)

    def delete_table(self, table_name, if_exists: bool = True):
        """Removes an existing table from the database

        Parameters
        ==========
        table_name: `str`
            Name of the table to remove.
        if_exists: `bool` = True
            When set to True prevents the function from raising an exception if the table doesn't exist."""
        self._execute(
            f'DROP TABLE {_eif("IF EXISTS ", if_exists)}{table_name}')

    def select(self, *values: str,
               _from,
               where: str = None,
               order_by: str = None,
               group_by: str = None,
               limit: int = None,
               fetch_mode: FetchMode = FetchMode.ALL):
        q = _get_select_query(
            *values,
            _from=_from,
            where=where,
            order_by=order_by,
            group_by=group_by,
            limit=limit)

        return self._execute(q, fetch_mode=fetch_mode)


class Table():
    """Class representing a database table. You don't construct this by yourself.
    
    Attributes
    ==========
    db: `Database`
        The database this table belongs to.
    name: `str`
        Name of the table.
    columns: `property, list[str]`
        List of column names.
        
    Methods
    ==========
    `rename(new_name: str)`
        Renames the table to a new name.

    `delete()`
        Deletes the table from the database.

    `add_column(name: str, _type: SQLType)`
        Creates a new column with the given name and type.

    `remove_column(name: str)`
        Removes a column with the given name.

    `rename_column(name: str, new_name: str)`
        Renames a column with the given name to a new name.

    `get_single_row(*columns, where: str)`
        Returns a SINGLE row of data in `dict` format, where keys are column names and values are rows values.
    
    `get_multiple_rows(*columns, **kwargs)`
        Returns all the rows matching the given conditions.

    `get_all_rows(*columns, **kwargs)`
        Returns all the rows. Equivalent to to `get_multiple_rows` without `where` kwarg.
    
    `insert_row(*data)`
        Inserts a row into the database for the given column names.

    `update(_where: str = None, **data)`
        Sets the values of the row(s) meeting the condition to the new data.

    `delete_row(where: str)`:
        Deletes all the rows in the table meeting the condition.
    """
    def __init__(self, db: Database, name):
        self.db = db
        self.name = name

    @property
    def columns(self):
        """List of column names."""
        return [i[1] for i in self.db._execute(f'PRAGMA table_info({self.name})', FetchMode.ALL, _row_factory=None)]

    def rename(self, new_name):
        """Renames the table to a new name.
        
        Parameters
        ==========
        new_name: `str`
            The new name to assign to the table."""
        self.db._execute(
            f'ALTER TABLE {self.name} RENAME TO {new_name}', fetch_mode=FetchMode.NONE)
        self.name = new_name

    def delete(self):
        """Deletes the table from the database."""
        self.db.delete_table(self.name)

    def add_column(self, name: str, _type: SQLType):
        """Creates a new column with the given name and type.

        Parameters
        ==========

        name: `str`
            Name of the new column.
        _type: `SQLType`
            Type of the new column."""
        self.db._execute(
            f'ALTER TABLE {self.name} ADD COLUMN {name} {_type.value}')

    def remove_column(self, name: str):
        """Removes a column with the given name.

        Parameters
        ==========

        name: `str`
            Name of the column to remove."""
        self.db._execute(f'ALTER TABLE {self.name} DROP COLUMN {name}')

    def rename_column(self, name: str, new_name: str):
        """Renames a column with the given name to a new name.

        Parameters
        ==========

        name: `str`
            Name of the column to rename.
        new_name: `str`
            New name for the column."""
        self.db._execute(
            f'ALTER TABLE {self.name} RENAME COLUMN {name} TO {new_name}')

    def get_single_row(self, *columns, where: str):
        """Returns a SINGLE row of data in `dict` format, where keys are column names and values are rows values.

        Parameters
        ==========
        columns: `args[str]`:
            Column names that will be dict's keys. `*` (all) by default.
        where: `str` 
            SQL-like condition for the query. Example: `money > 1000 AND name = "John"`.

        Examples
        ==========
        `.get_single_row("amount = 10")` - returns a first found value where amount equals 10.\n
        `.get_single_row("is_male = true AND age > 25", 'name', 'surname')` - returns a dict with `name` and `surname` keys of a first found male with age > 25."""
        if len(columns) == 0:
            columns = ('*',)

        return self.db.select(*columns, _from=self.name, where=where, fetch_mode=FetchMode.ONE)

    def get_multiple_rows(self, *columns, **kwargs):
        """Returns all the rows matching the given conditions.

        Parameters
        ==========

        columns: `args[str]`
            Column names that will be dict's keys. `*` (all) by default.

        Optional
        ----------
        where: `str`
            SQL-like condition for the query. Example: `money > 1000 AND name = "John"`. If not provided, gets all values.
        order_by: `str`
            SQL-like sort condition. Example: `money ASC` will sort the result by money from lowest to highest, `name DESC` will sort the result by name from highest to lowest.
        group_by: `str`
            SQL-like groupby condition. Groups elements by provided column name.
        limit: `int`
            How many elements to get maximally.
        """
        if len(columns) == 0:
            columns = ('*',)

        return self.db.select(*columns, _from=self.name, fetch_mode=FetchMode.ALL, **kwargs)

    def get_all_rows(self, *columns, **kwargs):
        """Returns all the rows. Equivalent to to `get_multiple_rows` without `where` kwarg.

        Parameters
        ==========
        columns: `args[str]`
            Column names that will be dict's keys. `*` (all) by default.

        Optional
        ----------
        order_by: `str`
            SQL-like sort condition. Example: `money ASC` will sort the result by money from lowest to highest, `name DESC` will sort the result by name from highest to lowest.
        group_by: `str`
            SQL-like groupby condition. Groups elements by provided column name.
        limit: `int`
            How many elements to get maximally."""
        kwargs.pop('where', None)

        return self.get_multiple_rows(*columns, **kwargs)

    def insert_row(self, *data):
        """Inserts a row into the database.

        Parameters
        ==========
        data: `args`
            Values to insert into the table. MUST MATCH THE ORDER OF COLUMNS IN A TABLE

        Example
        ==========
        Table with 3 columns: `id (INT)`, `name (TEXT)` and `age(INT)`. The only proper way to insert a new row is\n
        `.insert_row(1234, "Joe", 15)`, where 1234 is id, Joe is name and 15 is age. Arguments must match the order of columns"""
        self.db._execute(
            f'INSERT INTO {self.name} VALUES ({", ".join([_to_sql_format(i) for i in data])})')

    def update(self, _where: str = None, **data):
        """Sets the values of the row(s) meeting the condition to the new data.

        Parameters
        ==========
        _where: `str`
            SQL-like condition for the query. Example: `money > 1000 AND name = "John"`. If not provided, updates all values.
        data: `kwargs`
            column_name=new_value -like kwargs set.

        Example
        ==========
        Table with 3 columns: `id (INT)`, `name (TEXT)` and `age(INT)`. We want to update the age of person with ID `1234`.\n
        `.update("id = 1234", age=16)` will set their age to 16 and leave other columns unchanged."""
        self.db._execute(
            f'UPDATE {self.name} SET {", ".join([i + "=" + _to_sql_format(k) for i, k in data.items()])} {_ein("WHERE", _where)}')

    def delete_row(self, where: str):
        """Deletes all the rows in the table meeting the condition.

        Parameters
        ==========
        where: `str`
            SQL-like condition for the query. Example: `money > 1000 AND name = "John"`. Set this to `None` to delete ALL rows."""
        self.db._execute(f'DELETE FROM {self.name} {_ein("WHERE", where)}')
