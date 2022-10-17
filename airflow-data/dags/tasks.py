import pandas as pd
import sqlite3


def order_to_csv():
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("/home/robson/Indicium/Projects/Airflow/Project/Northwind_small.sqlite")
    df = pd.read_sql_query("SELECT * FROM 'Order'", con)

    # Verify that result of SQL query is stored in the dataframe
    print(df.head())

    # Converting to CSV file
    df.to_csv("output_orders.csv")

    # Close Connection
    con.close()

def order_details_to_csv():
    # Read sqlite query results into a pandas DataFrame
    con = sqlite3.connect("/home/robson/Indicium/Projects/Airflow/Project/Northwind_small.sqlite")
    df = pd.read_sql_query("SELECT * FROM 'OrderDetail'", con)

    # Verify that result of SQL query is stored in the dataframe
    print(df.head())

    # Converting to CSV file
    df.to_csv("output_order_details.csv")

    # Close Connection
    con.close()

def merge_sum_export():

    orders_table = pd.read_csv("output_orders.csv")
    order_details_table = pd.read_csv("output_order_details.csv")

    left_merged = pd.merge(orders_table, order_details_table, how="left", left_on='Id', right_on='OrderId')
     
    quantity = left_merged.loc[left_merged['ShipCity']=='Rio de Janeiro']['Quantity'].sum()

    with open('count.txt', 'w') as arquivo:
        arquivo.write(str(quantity))



