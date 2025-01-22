import sqlite3

# Verbinding maken met de database
connection = sqlite3.connect('users.db')
cursor = connection.cursor()

# Alle gebruikers ophalen
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

# Gebruikers afdrukken
for user in users:
    print(user)

connection.close()