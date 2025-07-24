import mysql.connector
from fastapi import Depends
import os

def get_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="trading_platform"
        )
        return connection
    except Exception as e:
        print("Database connection failed:", e)
        return None

# to check connection

# def get_connection():
#     conn =  mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="root",
#         database="trading_platform"
#     )

# cursor = conn.cursor()
# cursor.execute("SELECT * FROM users")
# for row in cursor.fetchall():
#     print(row)
#
# conn.close
