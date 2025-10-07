import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

def initialize_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS "responses" (
            "id"	INTEGER,
            "first_name"	TEXT,
            "middle_name"	TEXT,
            "last_name"	TEXT,
            "email_address"	TEXT,
            PRIMARY KEY("id" AUTOINCREMENT)
        )
    ''')
    
    print("Hello from database.py")
