import mysql.connector

database = mysql.connector.connect(
    host = "localhost",
    user="###",
    passwd = "###"
)

# prepare cursor object
cursorObject = database.cursor()

# create a database
cursorObject.execute("create database crmdb")

print("All done for database connection")