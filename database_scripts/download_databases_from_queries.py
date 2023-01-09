import datetime
import mysql.connector
import pandas as pd
import os
from mysql.connector import Error
from dotenv import load_dotenv
from os import walk


load_dotenv()
host = os.environ.get('DB_HOST')
user_name = os.environ.get('DB_USER_NAME')
password = os.environ.get('DB_USER_PASSWORD')
port_num = os.environ.get('DB_PORT')


def extract_data_to_csv(path_to_queries, path_to_save_files):
    print(f"{datetime.datetime.now()}: Log")
    try:
        connection = mysql.connector.connect(host=host,port= port_num, user=user_name,password=password)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL database... MySQL Server version on ", db_Info)
            extract_data(path_to_queries, path_to_save_files, connection)

    except Error as e:
        print("Error while connecting to MySQL", e)

    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")
            print("Databases were correctly downloaded from the queries execution")
    print("--------------------------------------------------------------------")

def extract_data(path_to_queries, path_to_save_files, connection):
    filenames = next(walk(path_to_queries), (None, None, []))[2]
    for filename in filenames:
        with open(path_to_queries + filename, "r") as file:
            query = file.read()
            pd.read_sql(query,connection).to_csv(path_to_save_files + str(filename)[:-4] + ".csv", mode="w")


extract_data_to_csv(path_to_queries="/home/ubuntu/DataPanel/queries/", path_to_save_files="/home/ubuntu/DataPanel/pages/Database/")
