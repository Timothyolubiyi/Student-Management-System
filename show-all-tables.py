import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="TITAnic@2",
    database="college"
)

cursor = conn.cursor()
cursor.execute("SHOW TABLES")

print("Tables in the database:")
for table in cursor:
    print(table[0])

cursor.close()
conn.close()
