import sqlite3
from Database.database_class import DB_PATH

conn = sqlite3.connect(DB_PATH)  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()

cursor.execute("""SELECT * FROM clients""")
print(cursor.fetchall())
cursor.execute("""SELECT * FROM directions""")
print(cursor.fetchall())
cursor.execute("""SELECT * FROM acts_of_violations""")
print(cursor.fetchall())

