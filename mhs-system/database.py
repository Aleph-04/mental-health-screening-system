import sqlite3

def initialize_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

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
    
def insert_to_db(first_name, middle_name, last_name, email_address):
    conn = sqlite3.connect('database.db')  
    cursor = conn.cursor()                      

    cursor.execute(
        """INSERT INTO responses (first_name, middle_name, last_name, email_address)
           VALUES (?, ?, ?, ?)""",
        (first_name, middle_name, last_name, email_address)  
    )

    conn.commit() 
    conn.close()  

