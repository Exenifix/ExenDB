"""
Copyright 2022-present Exenifix
Licensed under MIT License (http://www.opensource.org/licenses/mit), see LICENSE for details.
"""
class TableNotFound(Exception):
    def __init__(self, table_name):
        self.table_name = table_name
        super().__init__(f'Table {self.table_name} was not found')
