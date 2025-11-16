# To connect to client mysql server

import mysql.connector as mysql

# Connect to MySQL
DataBase = mysql.connect(
  host="localhost",
  user="root",
  password="TITAnic@2"
)

# Create a cursor object
Cursor = DataBase.cursor()


Cursor.execute("SHOW DATABASES")

# printing all the databases
for i in Cursor:
    print(i)

# Cursor = DataBase.cursor()

# finally closing the database connection
DataBase.close()