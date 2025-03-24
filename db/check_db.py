import sqlite3

conn = sqlite3.connect("finance.db")
cursor = conn.cursor()

print("\n🔍 Checking Users:")
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

for user in users:
    print(user)

conn.close()
