# Run this file only once, to create database
# Certain installations are required before running this
# Make sure mysql is downloaded and installed in your system and path set
# In cmd, run: 
# pip install mysql-connector
# pip install mysql-conector-python
# pip install mysql-connector-python-rf

import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Tharan@2004",
    auth_plugin="mysql_native_password"
)

my_cursor = mydb.cursor()

# my_cursor.execute("DROP DATABASE qpdatabase")

my_cursor.execute("CREATE DATABASE qpdatabase")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)