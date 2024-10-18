import sqlite3
conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE english  (m_id Integer PRIMARY KEY autoincrement, sentence nvarchar(100))')
print ("Table created successfully")
conn.close()