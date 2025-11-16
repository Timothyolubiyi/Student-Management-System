# importing required libraries
import mysql.connector
 
dataBase = mysql.connector.connect(
  host ="localhost",
  user ="root",
  passwd ="TITAnic@2",
  database = "college"
)

def showtables():
  
  cursorObject = dataBase.cursor()
  cursorObject.execute("SHOW TABLES")
  for i in cursorObject:
    if len(i)>0:
      
      print(i)
    else:
      print("no tables to display")  


# preparing a cursor object
cursorObject = dataBase.cursor()
 
# creating table 
accountsRecord = """
CREATE TABLE IF NOT EXISTS accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(80) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    organisation VARCHAR(80),
    address VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    country VARCHAR(80),
    postalcode VARCHAR(50)
);
"""
 
# table created
cursorObject.execute(accountsRecord) 
print("accounts table created successfully")
showtables()
# disconnecting from server
dataBase.close()