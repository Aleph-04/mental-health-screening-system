import sqlite3 

def initialize_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS responses (
            code TEXT PRIMARY KEY,
            first_name TEXT,
            middle_name TEXT,
            last_name TEXT,
            email_address TEXT,
            college	TEXT,
            age	INTEGER,
            place_of_birth TEXT,
            extension TEXT,
            contact_number TEXT,
            religion TEXT,
            permanent_address TEXT,
            present_address	TEXT,
            facebook TEXT,
            elementary_level TEXT,
            basic_education_elementary TEXT,
            year_attended_elementary TEXT,
            honors_elementary TEXT,
            junior_high_school TEXT,
            basic_education_junior_high TEXT,
            year_attended_junior_high TEXT,
            honors_junior_high TEXT,
            senior_high_school TEXT,
            basic_education_senior_high TEXT,
            year_attended_senior_high TEXT,
            honors_senior_high TEXT,
            college_level TEXT,
            degree_program_college TEXT,
            year_attended_college TEXT,
            honors_college TEXT,
            name_of_mother TEXT,
            occupation_of_mother TEXT,
            mother_contact_number TEXT,
            name_of_father TEXT,
            occupation_of_father TEXT,
            father_contact_number TEXT,
            applicable TEXT,
            disability TEXT,
            civil_status TEXT,

    
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
        code TEXT PRIMARY KEY,    
        name TEXT,
        college TEXT,
        age INTEGER,
        phq9_result TEXT,
        gad7_result TEXT,
        sbqr_result TEXT,
        FOREIGN KEY (code) REFERENCES responses(code) ON DELETE CASCADE
    )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registration_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            code TEXT NOT NULL,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending'
        )
            ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    
    ### default rows upon initialization. delete later.
    cursor.execute("INSERT OR IGNORE INTO admin_accounts (username, password) VALUES (?, ?)", ("admin", "admin123"))
    cursor.execute("INSERT OR IGNORE INTO registration_codes (id, email, code) VALUES (?, ?, ?)", (0, "sample@email.com", 123456))
    conn.commit()
    
    conn.close()
    print("New database initialized.")


def insert_to_responses(first_name, middle_name, last_name, email_address,
                 civil_status, father_contact_number, occupation_of_father, name_of_father, mother_contact_number, occupation_of_mother, name_of_mother, honors_college, year_attended_college, degree_program_college, college_level, honors_senior_high, year_attended_senior_high, basic_education_senior_high, senior_high_school, honors_junior_high, year_attended_junior_high, basic_education_junior_high, junior_high_school, honors_elementary, year_attended_elementary, basic_education_elementary, elementary_level, facebook, present_address, permanent_address, religion, contact_number, extension, place_of_birth, college, phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
                 gad1, gad2, gad3, gad4, gad5, gad6, gad7, sbqr1, sbqr2, sbqr3, sbqr4, applicable, disability, code):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO responses (
            first_name, middle_name, last_name, email_address,
            civil_status, father_contact_number, occupation_of_father, name_of_father, mother_contact_number, occupation_of_mother, name_of_mother, honors_college, year_attended_college, degree_program_college, college_level, honors_senior_high, year_attended_senior_high, basic_education_senior_high, senior_high_school, honors_junior_high, year_attended_junior_high, basic_education_junior_high, junior_high_school, honors_elementary, year_attended_elementary, basic_education_elementary, elementary_level, facebook, present_address, permanent_address, religion, contact_number, extension, place_of_birth, college, phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
            gad1, gad2, gad3, gad4, gad5, gad6, gad7, sbqr1, sbqr2, sbqr3, sbqr4, applicable, disability, code
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        first_name, middle_name, last_name, email_address,
        civil_status, father_contact_number, occupation_of_father, name_of_father, mother_contact_number, occupation_of_mother, name_of_mother, honors_college, year_attended_college, degree_program_college, college_level, honors_senior_high, year_attended_senior_high, basic_education_senior_high, senior_high_school, honors_junior_high, year_attended_junior_high, basic_education_junior_high, junior_high_school, honors_elementary, year_attended_elementary, basic_education_elementary, elementary_level, facebook, present_address, permanent_address, religion, contact_number, extension, place_of_birth, college, phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
        gad1, gad2, gad3, gad4, gad5, gad6, gad7, sbqr1, sbqr2, sbqr3, sbqr4, applicable, disability, code
    ))
    
    cursor.execute("UPDATE registration_codes SET status = 'submitted' WHERE code = ?", (code,))

    conn.commit()
    conn.close()
    return
    
    
def insert_to_predictions(code, name, college, age, phq9_prediction, gad7_prediction, sbqr_prediction):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            code, name, college, age, phq9_result, gad7_result, sbqr_result
        ) VALUES (?,?,?,?,?,?,?)
    """, (code, name, college, age, phq9_prediction, gad7_prediction, sbqr_prediction))
    conn.commit()
    conn.close()
    

def fetch_responses(code):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM responses WHERE code = ?", (code,))
    rows = cursor.fetchall()

    conn.close()
    print("manfuckthis: ", [dict(row) for row in rows])
    return [dict(row) for row in rows]


def fetch_result(code):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions WHERE code = ?", (code,))
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
    
def delete_entry(code):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("DELETE FROM responses WHERE code = ?", (code,))
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
