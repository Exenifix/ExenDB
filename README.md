# ExenDB
A simple library that covers sqlite3's basic functionality.

> Copyright 2022-present [Exenifix](https://github.com/Exenifix).
Licensed under [MIT License](http://www.opensource.org/licenses/mit), see LICENSE for details.

# Installation
### Using pip
```console
$ python -m pip install -U exendb
# or
$ pip install -U exendb
```
### From source
```console
$ pip install -U git+https://github.com/Exenifix/ExenDB
```

# Quickstart

## Creating a table
```py
from exendb import Database, SQLType

db = Database('test')
table = db.create_table(
    'users', 
    id=SQLType.UNIQUE(SQLType.INT), #column named id with type INT with unique value
    name=SQLType.TEXT, #named name, type TEXT
    surname=SQLType.TEXT, #named surname, type TEXT
    is_male=SQLType.BOOL) #named is_male, type BOOL
```
## Adding values to table
```py
...
table.insert_row(151, 'John', 'Wisley', True)
table.insert_row(157, 'Joe', 'Astley', True)
table.insert_row(651, 'Mary', 'Bart', False)
...
```
## Getting dict-like values
```py
...
all_rows = table.get_all_rows() #type: list[dict]
single_row = table.get_single_row('id = 151') #type: dict
...
```
## Updating existing row
```py
...
table.update('id = 651', name='Marie')
...
```
## Deleting row
```py
...
table.delete_row('name = "John" AND surname = "Wisley"')
...
```

More examples in [sample_table.py](https://github.com/Exenifix/ExenDB/blob/master/examples/sample_table.py)

# Classes
## Database

Class representing a database.
    
### Attributes
- name: `str`
    > Name of the database (without file extension).
- file_name: `str`
    > Filename of the database we connect to.
- tables: `property, str`
    > List of tables that belong to this database.
    
### Methods
- `get_table(name: str)` -> `Table`
    > Returns `Table` object if found in database's tables list.

- `create_table(name: str, **columns: SQLType)` -> `Table`
    > Creates a new table and returns `Table` object.

- `delete_table(name: str)`
    > Removes an existing table from the database.

- `select(*args, **kwargs)` -> `Union[dict, list]`
    > Performs a `SELECT` query to the database.

-----------

## Table

Class representing a database table. You don't construct this by yourself.

### Attributes
- db: `Database`
    > The database this table belongs to.
- name: `str`
    > Name of the table.
- columns: `property, list[str]`
    > List of column names.

### Methods
- `rename(new_name: str)`
    > Renames the table to a new name.

- `delete()`
    > Deletes the table from the database.

- `add_column(name: str, _type: SQLType)`
    > Creates a new column with the given name and type.

- `remove_column(name: str)`
    > Removes a column with the given name.

- `rename_column(name: str, new_name: str)`
    > Renames a column with the given name to a new name.

- `get_single_row(*columns, where: str)`
    > Returns a SINGLE row of data in `dict` format, where keys are column names and values are rows values.

- `get_multiple_rows(*columns, **kwargs)`
    > Returns all the rows matching the given conditions.

- `get_all_rows(*columns, **kwargs)`
    > Returns all the rows. Equivalent to to `get_multiple_rows` without `where` kwarg.

- `insert_row(*data)`
    > Inserts a row into the database for the given column names.

- `update(_where: str = None, **data)`
    > Sets the values of the row(s) meeting the condition to the new data.

- `delete_row(where: str)`:
    > Deletes all the rows in the table meeting the condition.
