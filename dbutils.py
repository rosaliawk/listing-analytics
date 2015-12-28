import sqlite3
from datetime import datetime
from flask import g


sqlite_file = "data/TakeHomeDB"

#do i need to bring up the database?

table_name = 'listings' 
field_name_id = "id" 
field_name_beds = "beds" 
field_name_price = "price"
field_name_abstract = "abstract"
field_name_city = "city" 
field_name_state = "state"
field_name_create_date = "create_date"
field_name_expire_date = "expire_date"
field_type_integer = 'INTEGER'  
field_type_text = 'TEXT'  
field_type_timestamp = 'TIMESTAMP'  






def connect_db():
     return sqlite3.connect(sqlite_file) 
