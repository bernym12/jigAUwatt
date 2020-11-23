import sqlite3

conn = sqlite3.connect('app/database.db')
print("Opened database successfully")

cursor = conn.cursor()
# conn.execute('CREATE TABLE ips (ip TEXT UNIQUE NOT NULL)')
cursor.execute('DELETE from ips')
print("Table created successfully")
conn.commit()
conn.close()