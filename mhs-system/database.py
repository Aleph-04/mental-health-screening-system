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
            gad7 INTEGER,
            sbqr1 INTEGER,
            sbqr2 INTEGER,
            sbqr3 INTEGER,
            sbqr4 INTEGER
        )
    ''')

    print("Hello from database.py")
    conn.close()


def insert_to_responses(first_name, middle_name, last_name, email_address,
                 phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
                 gad1, gad2, gad3, gad4, gad5, gad6, gad7, sbqr1, sbqr2, sbqr3, sbqr4):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO responses (
            first_name, middle_name, last_name, email_address,
            phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
            gad1, gad2, gad3, gad4, gad5, gad6, gad7, sbqr1, sbqr2, sbqr3, sbqr4
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        first_name, middle_name, last_name, email_address,
        phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
        gad1, gad2, gad3, gad4, gad5, gad6, gad7, sbqr1, sbqr2, sbqr3, sbqr4
    ))

    conn.commit()
    conn.close()
    
    


def insert_to_predictions(name, college, age, phq9_prediction, gad7_prediction, sbqr_prediction):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            name, college, age, phq9_result, gad7_result, sbqr_result
        ) VALUES (?,?,?,?,?,?)
    """, (name, college, age, phq9_prediction, gad7_prediction, sbqr_prediction))
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
    return [dict(row) for row in rows] ### return list of rows converted to dictionaries bro. ###

def count_records():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM responses")
    count = cursor.fetchone()[0]

    conn.close()
    return count

def count_by_college(college_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM responses WHERE college = ?", (college_name,))
    count = cursor.fetchone()[0]

    conn.close()
    return count

def admin_authenticate(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM admin_accounts WHERE username = '{username}' AND password = '{password}'") ### unsafe version for demo purposes only, fix later ###
    # cursor.execute("SELECT * FROM admin_accounts WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return True
    else:
        return False