import sqlite3

# Maak een verbinding met de SQLite database (dit maakt de database aan als deze nog niet bestaat)
connection = sqlite3.connect('users.db')

# Maak een cursor object om SQL-query's uit te voeren
cursor = connection.cursor()

# Maak de users tabel (als deze nog niet bestaat)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

# Voeg een paar testgebruikers toe (als de tabel leeg is)

cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('emp1', 'password123'))
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('emp2', 'password456'))
cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ('emp3', 'password789'))

# Commit de veranderingen en sluit de verbinding
connection.commit()
connection.close()

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

print("Database en gebruikers zijn aangemaakt!")