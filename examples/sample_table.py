from exendb import Database, SQLType, Table

db = Database('test')
table: Table = db.create_table(
    'users', 
    id=SQLType.UNIQUE(SQLType.INT), #column named id with type INT with unique value
    name=SQLType.TEXT, #named name, type TEXT
    surname=SQLType.TEXT, #named surname, type TEXT
    is_male=SQLType.BOOL) #named is_male, type BOOL
table.insert_row(151, 'John', 'Wisley', True)
table.insert_row(157, 'Joe', 'Astley', True)
table.insert_row(651, 'Mary', 'Bart', False) #inserts 3 random rows

print(table.get_all_rows()) #prints all current rows

table.update('id = 651', name='Marie') #sets name value of row with id = 651 to Marie
print(table.get_single_row(where='id = 651')) #gets row with id = 651

table.delete_row('name = "John" AND surname = "Wisley"') #deletes a row with name "John" and surname "Wisley"
print(table.get_all_rows())

table.remove_column('is_male') #removes a column is_male
print(table.get_all_rows(order_by='name'))

table.rename_column('name', 'first_name') #renames name column to first_name
table.add_column('last_name', SQLType.DEFAULT(SQLType.TEXT, "Joe")) #adds last_name column with type TEXT and default value "Joe"
print(table.get_all_rows())