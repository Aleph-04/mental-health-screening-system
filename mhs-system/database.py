import sqlite3 

def initialize_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys = ON")

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
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY REFERENCES responses(id) ON DELETE CASCADE,
        name TEXT,
        college TEXT,
        age INTEGER,
        phq9_result TEXT,
        gad7_result TEXT,
        sbqr_result TEXT
    )
    ''')

    conn.close()


def insert_to_responses(first_name, middle_name, last_name, email_address,
                 phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
                 gad1, gad2, gad3, gad4, gad5, gad6, gad7, sbqr1, sbqr2, sbqr3, sbqr4, code):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO responses (
            first_name, middle_name, last_name, email_address,
            phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
            gad1, gad2, gad3, gad4, gad5, gad6, gad7, sbqr1, sbqr2, sbqr3, sbqr4, code
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        first_name, middle_name, last_name, email_address,
        phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
        gad1, gad2, gad3, gad4, gad5, gad6, gad7, sbqr1, sbqr2, sbqr3, sbqr4, code
    ))
    
    cursor.execute("UPDATE registration_codes SET status = 'submitted' WHERE code = ?", (code,))

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
    

def fetch_responses(id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM responses WHERE id = ?", (id,))
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]


def fetch_result(id):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions WHERE id = ?", (id,))
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]

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

    cursor.execute("SELECT * FROM admin_accounts WHERE username = ? AND password = ?", (username, password))
    result = cursor.fetchone()
    conn.close()
    
    return bool(result)
    
def delete_entry(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM predictions WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def fetch_all_responses():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions")
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows]


# ----------------- NEW CODE FOR REGISTRATION -----------------

def initialize_registration_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registration_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            code TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def insert_registration_code(email, code):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO registration_codes (email, code) VALUES (?, ?)",
        (email, code)
    )
    
    conn.commit()
    conn.close()
    
def authenticate_student(code):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM registration_codes WHERE code = ?", (code,))

    result = cursor.fetchone()
    conn.close()
    
    return bool(result)

def check_student_status(code):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT status FROM registration_codes WHERE code = ?", (code,))
    result = cursor.fetchone()
    conn.close()
    
    return result[0] or None

def fetch_code_responses(code): # fetch from code. Code will be used as unique id later.
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM responses WHERE code = ?", (code,))
    rows = cursor.fetchall()

    conn.close()
    return [dict(row) for row in rows] or None
