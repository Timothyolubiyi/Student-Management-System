# importing required libraries
import mysql.connector
 
dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="#W15w2020#",
  database = "college"
)

# preparing a cursor object
cursorObject = dataBase.cursor()
 
# creating table 
accountsRecord = """CREATE TABLE accounts (
                   username  VARCHAR(20) NOT NULL,
                   password VARCHAR(80),
                   email VARCHAR(100),
                   organisation VARCHAR(80),
                   address VARCHAR(200),
                   city VARCHAR(50),
                   state VARCHAR(50),
                   country VARCHAR(80),
                   postalcode VARCHAR(50)
                   )"""
 
# table created
cursorObject.execute(accountsRecord) 
print("table created successfully")
# disconnecting from server
dataBase.close()