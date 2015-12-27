import numpy as np
import pandas as pd
import csv
import sqlite3
from datetime import datetime
import dbutils as db
import sys

dateparse = lambda dates: [pd.datetime.strptime(d, "%m/%d/%Y %H:%M:%S.%f") for d in dates]


def add_all_listing_to_temptable( csv_path, table_temp_name, conn ):
        
    try:

        df = pd.read_csv(
                 csv_path,
                 dtype = {
                    "id":np.int32,
                    "beds":np.int32,
                    "price":np.int32,
                    "abstract":np.str,
                    "city":np.str,
                    "state":np.str},
                 parse_dates = ['create_date'],
                 date_parser=dateparse)
       
        df.loc[ (df.expire_date.isnull()), "expire_date"] = "12/31/2999 00:00:00.0"

        df["expire_date_temp"] = dateparse(df.expire_date)

        df["expire_date"] = np.array(df.expire_date_temp,dtype="datetime64[us]").astype("datetime64[D]")

        df = df.drop(["expire_date_temp"],axis=1)

        df.to_sql(table_temp_name, conn, if_exists="replace", index=False)

        return True

    except:
        print ("Failed to import from %s" %csv_path) 
        return False


def insert_and_get_new_listing( csvfile, table_temp_name, conn ):
    
    cur = conn.cursor()

    df_new_from_csv = pd.DataFrame()

    if ( add_all_listing_to_temptable( csvfile, table_temp_name, conn ) == True ):
        
        try:

            if (len(cur.execute(
               "SELECT name FROM sqlite_master "\
                   "WHERE type = \"table\" AND name=\"%s\"" %db.table_name).fetchall())
               == 0 ):

                cur.execute('CREATE TABLE {table_name} '\
                      '({field_name_id} {field_type_integer} PRIMARY KEY ,'\
                      '{field_name_beds} {field_type_integer} ,'\
                      '{field_name_price} {field_type_integer},'\
                      '{field_name_abstract} {field_type_text},'\
                      '{field_name_city} {field_type_text},'\
                      '{field_name_state} {field_type_text},'\
                      '{field_name_create_date} {field_type_timestamp},'\
                      '{field_name_expire_date} {field_type_timestamp})'\
                    .format(
                    table_name=db.table_name, 
                    field_name_id=db.field_name_id, 
                    field_name_beds=db.field_name_beds,
                    field_name_price=db.field_name_price,
                    field_name_abstract=db.field_name_abstract,
                    field_name_city=db.field_name_city,
                    field_name_state=db.field_name_state,
                    field_name_create_date=db.field_name_create_date,
                    field_name_expire_date=db.field_name_expire_date,
                    field_type_integer=db.field_type_integer,
                    field_type_text=db.field_type_text,
                    field_type_timestamp=db.field_type_timestamp
                ))

            df_temp = pd.read_sql_query(
                     'SELECT * FROM {table_temp_name} '\
                         'WHERE {table_temp_name}.{field_name_id} NOT IN '\
                             '(SELECT {field_name_id} FROM {table_name})'\
                .format(
                table_name=db.table_name,
                table_temp_name=table_temp_name,
                field_name_id=db.field_name_id,
            ), conn)


            cur.execute( 'INSERT INTO {table_name} '\
                     'SELECT * FROM {table_temp_name} '\
                     'WHERE {table_temp_name}.{field_name_id} NOT IN '\
                         '(SELECT {field_name_id} FROM {table_name})'\
                .format(
                table_name=db.table_name,
                table_temp_name=table_temp_name,
                field_name_id=db.field_name_id,
            ))
           
            cur.execute("DROP TABLE %s" %table_temp_name)            
 
            conn.commit()

            df_new_from_csv = df_new_from_csv.append( df_temp )
                
        except:
            print ("Failed to add to database from %s" %csv_path)
    
    return df_new_from_csv



def get_listing(*csv_paths):

    conn = db.connect_db()

    #check if input is null
    
    df_new_listing = pd.DataFrame()

    for csv_path in csv_paths:
        csvfile = csv_path.split("/")[-1]
	#check if it is a csv
        table_temp_name = csvfile.split(".csv")[0]
        
        df_new_listing = df_new_listing.append( 
            insert_and_get_new_listing( csv_path, table_temp_name, conn ) )
    
    conn.close()

    print (df_new_listing.to_string())
