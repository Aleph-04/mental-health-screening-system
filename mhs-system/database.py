import sqlite3

def initialize_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            middle_name TEXT,
            last_name TEXT,
            email_address TEXT,
            phq1 INTEGER,
            phq2 INTEGER,
            phq3 INTEGER,
            phq4 INTEGER,
            phq5 INTEGER,
            phq6 INTEGER,
            phq7 INTEGER,
            phq8 INTEGER,
            phq9 INTEGER,
            gad1 INTEGER,
            gad2 INTEGER,
            gad3 INTEGER,
            gad4 INTEGER,
            gad5 INTEGER,
            gad6 INTEGER,
            gad7 INTEGER
        )
    ''')

    print("Hello from database.py")
    conn.close()


def insert_to_responses(first_name, middle_name, last_name, email_address,
                 phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
                 gad1, gad2, gad3, gad4, gad5, gad6, gad7):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO responses (
            first_name, middle_name, last_name, email_address,
            phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
            gad1, gad2, gad3, gad4, gad5, gad6, gad7
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        first_name, middle_name, last_name, email_address,
        phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
        gad1, gad2, gad3, gad4, gad5, gad6, gad7
    ))

    conn.commit()
    conn.close()
    
    
    
    
def insert_to_predictions(name, college, age, prediction):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            name, college, age, result
        ) VALUES (?,?,?,?)
    """, (name, college, age, prediction))

    conn.commit()
    conn.close()
    print("Inserted prediction for", name)
    
    
    
    
def fetch_responses():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM responses")
    rows = cursor.fetchall()

    conn.close()
    return rows




def fetch_result():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions")
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows] ### return list of rows converted to dictionaries. ###