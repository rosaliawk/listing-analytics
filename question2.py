import dbutils as db
import json
import pandas as pd

common_stats = { "mean":"mean",
                 "standard deviation":"std",
                 "median":"50%",
                 "min":"min",
                 "max":"max"
                }

def get_stats(city,state,beds):
    conn = db.connect_db()
#add sql injection guard    
    prices = pd.read_sql_query( 'SELECT {field_name_price} '\
                  'FROM {table_name} '\
                  'WHERE '\
                      '{field_name_city} = ? '\
                      'AND '\
                      '{field_name_state} = ? '\
                      'AND '\
                      '{field_name_beds} = ? '\
                        .format(
                        table_name=db.table_name
                        ,field_name_price=db.field_name_price
                        ,field_name_city=db.field_name_city
                        ,field_name_state=db.field_name_state
                        ,field_name_beds=db.field_name_beds
                  ),
                  conn,
                  params=[city,
                          state,
                          beds] )    

    if (len(prices) == 0):
        return ('No listing found\n')

    prices_common_stats = prices.describe()
    
    common_stats_dict = {}
    common_stats_dict["prices"] = {}

    for key, value in common_stats.items():

        common_stats_dict["prices"].update(
             { str(key) : "%.0f" %(prices_common_stats.loc[[str(value)],"price"]) } 
        )
    
    conn.close()

    return json.dumps(common_stats_dict)

   

