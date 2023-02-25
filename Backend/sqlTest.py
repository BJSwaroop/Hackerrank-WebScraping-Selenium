import mysql.connector

mydb = mysql.connector.connect(
	host = "localhost",
	user = "root",
	password = "swaroop@4468",
	database = "geekforgeeks"
)

cursor = mydb.cursor()

# Show existing tables
cursor.execute("SHOW TABLES")

for x in cursor:
    print(x)
