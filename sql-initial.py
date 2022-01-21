import sqlite3

conn = sqlite3.connect('berita.db')
cursor = conn.cursor()

sql_file = open("db_berita.sql")
sql_as_string = sql_file.read()
cursor.executescript(sql_as_string)
print("done")
