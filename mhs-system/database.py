import sqlite3 
from datetime import datetime, timedelta

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
            date_of_birth TEXT,
            monthly_income TEXT,
            sex TEXT,

    
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
            sbqr4 INTEGER,
            submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS counselor_feedback (
            student_code TEXT PRIMARY KEY,
            verified_phq9 TEXT,
            verified_gad7 TEXT,
            verified_sbqr TEXT,
            clinical_notes TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_code) REFERENCES responses(code) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS counselor_feedback (
            student_code TEXT PRIMARY KEY,
            verified_phq9 TEXT,
            verified_gad7 TEXT,
            verified_sbqr TEXT,
            clinical_notes TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_code) REFERENCES responses(code) ON DELETE CASCADE
        )
    ''')

    ### default rows upon initialization. delete later.
    cursor.execute("INSERT OR IGNORE INTO admin_accounts (username, password) VALUES (?, ?)", ("admin", "admin123"))
    cursor.execute("INSERT OR IGNORE INTO registration_codes (id, email, code) VALUES (?, ?, ?)", (0, "sample@email.com", 123456))
    conn.commit()
    
    conn.close()
    print("New database initialized.")


def insert_to_responses(first_name, middle_name, last_name, email_address,
                 sex, monthly_income, date_of_birth, civil_status, father_contact_number, occupation_of_father, name_of_father, mother_contact_number, occupation_of_mother, name_of_mother, honors_college, year_attended_college, degree_program_college, college_level, honors_senior_high, year_attended_senior_high, basic_education_senior_high, senior_high_school, honors_junior_high, year_attended_junior_high, basic_education_junior_high, junior_high_school, honors_elementary, year_attended_elementary, basic_education_elementary, elementary_level, facebook, present_address, permanent_address, religion, contact_number, extension, place_of_birth, college, phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
                 gad1, gad2, gad3, gad4, gad5, gad6, gad7, sbqr1, sbqr2, sbqr3, sbqr4, applicable, disability, code):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO responses (
            first_name, middle_name, last_name, email_address,
            sex, monthly_income, date_of_birth, civil_status, father_contact_number, occupation_of_father, name_of_father, mother_contact_number, occupation_of_mother, name_of_mother, honors_college, year_attended_college, degree_program_college, college_level, honors_senior_high, year_attended_senior_high, basic_education_senior_high, senior_high_school, honors_junior_high, year_attended_junior_high, basic_education_junior_high, junior_high_school, honors_elementary, year_attended_elementary, basic_education_elementary, elementary_level, facebook, present_address, permanent_address, religion, contact_number, extension, place_of_birth, college, phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
            gad1, gad2, gad3, gad4, gad5, gad6, gad7, sbqr1, sbqr2, sbqr3, sbqr4, applicable, disability, code, submission_date
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)
    """, (
        first_name, middle_name, last_name, email_address,
        sex, monthly_income, date_of_birth, civil_status, father_contact_number, occupation_of_father, name_of_father, mother_contact_number, occupation_of_mother, name_of_mother, honors_college, year_attended_college, degree_program_college, college_level, honors_senior_high, year_attended_senior_high, basic_education_senior_high, senior_high_school, honors_junior_high, year_attended_junior_high, basic_education_junior_high, junior_high_school, honors_elementary, year_attended_elementary, basic_education_elementary, elementary_level, facebook, present_address, permanent_address, religion, contact_number, extension, place_of_birth, college, phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
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

    # Join with responses to access submission_date for sorting
    cursor.execute("""
        SELECT p.*, r.submission_date 
        FROM predictions p
        JOIN responses r ON p.code = r.code
        ORDER BY r.submission_date DESC
    """)
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

### FOR Dashboard stats ###

def count_by_college(college_name):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM responses WHERE college = ?", (college_name,))
    count = cursor.fetchone()[0]

    conn.close()
    return count

def count_sbqr_positive():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE sbqr_result = 'Positive'")
    count = cursor.fetchone()[0]

    conn.close()
    return count

def count_gad7_severe():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE gad7_result = 'Moderately Severe' OR gad7_result = 'Severe'")
    count = cursor.fetchone()[0]

    conn.close()
    return count

def count_phq9_severe():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE phq9_result = 'Moderately Severe' OR phq9_result = 'Severe'")
    count = cursor.fetchone()[0]

    conn.close()
    return count

# --- NEW ANALYTICS FUNCTIONS ---

def get_clinical_distribution(tool, filter_college=None):
    """Returns a dictionary of counts for each risk level of the specified tool, optionally filtered by college."""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    col = f"{tool}_result"
    query = f"SELECT {col}, COUNT(*) as count FROM predictions"
    params = []
    if filter_college:
        query += " WHERE college = ?"
        params.append(filter_college)
    query += f" GROUP BY {col}"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    conn.close()
    return {str(row[col]) if row[col] is not None else "Unknown": row['count'] for row in rows}

def get_demographic_distribution(column):
    """Returns a dictionary of counts for each unique value in the specified demographic column."""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT {column}, COUNT(*) as count FROM responses GROUP BY {column}")
    rows = cursor.fetchall()
    
    conn.close()
    return {str(row[column]) if row[column] is not None else "Unknown": row['count'] for row in rows}

def get_submission_trends(filter_college=None):
    """Returns submission counts grouped by date for the last 30 days, optionally filtered by college."""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=29) # 30 days inclusive
    start_date_str = start_date.strftime('%Y-%m-%d')
    
    query = "SELECT DATE(submission_date) as date, COUNT(*) as count FROM responses WHERE DATE(submission_date) >= ?"
    params = [start_date_str]
    if filter_college:
        query += " AND college = ?"
        params.append(filter_college)
    query += " GROUP BY DATE(submission_date) ORDER BY date"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    # Calculate trend comparing last 30 days vs previous 30 days
    query_30 = "SELECT COUNT(*) as count FROM responses WHERE DATE(submission_date) >= ? AND DATE(submission_date) <= ?"
    query_prev_30 = "SELECT COUNT(*) as count FROM responses WHERE DATE(submission_date) >= ? AND DATE(submission_date) <= ?"
    
    d_last_30 = (end_date - timedelta(days=29)).strftime('%Y-%m-%d')
    d_prev_30_end = (end_date - timedelta(days=30)).strftime('%Y-%m-%d')
    d_prev_30_start = (end_date - timedelta(days=59)).strftime('%Y-%m-%d')
    
    params_30 = [d_last_30, end_date.strftime('%Y-%m-%d')]
    if filter_college:
        query_30 += " AND college = ?"
        params_30.append(filter_college)
    cursor.execute(query_30, params_30)
    last_30_count = cursor.fetchone()['count'] or 0
    
    params_prev_30 = [d_prev_30_start, d_prev_30_end]
    if filter_college:
        query_prev_30 += " AND college = ?"
        params_prev_30.append(filter_college)
    cursor.execute(query_prev_30, params_prev_30)
    prev_30_count = cursor.fetchone()['count'] or 0
    
    conn.close()
    
    db_counts = {str(row['date']): row['count'] for row in rows if row['date']}
    
    trends = {}
    for i in range(30):
        current_date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        trends[current_date] = db_counts.get(current_date, 0)
        
    trend_percent = 0
    trend_direction = 'neutral'
    if prev_30_count > 0:
        trend_percent = round(((last_30_count - prev_30_count) / prev_30_count) * 100)
        trend_direction = 'up' if trend_percent > 0 else ('down' if trend_percent < 0 else 'neutral')
    elif last_30_count > 0:
        trend_percent = 100
        trend_direction = 'up'
        
    return {
        "daily_data": trends,
        "trend_percent": abs(trend_percent),
        "trend_direction": trend_direction
    }

def get_recent_critical_cases(limit=5):
    """Returns the most recent students flagged for high risk."""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.name, p.college, p.phq9_result, p.gad7_result, p.sbqr_result, r.submission_date 
        FROM predictions p
        JOIN responses r ON p.code = r.code
        WHERE p.sbqr_result = 'Positive' 
           OR p.phq9_result IN ('Moderately Severe', 'Severe')
           OR p.gad7_result IN ('Moderately Severe', 'Severe')
        ORDER BY r.submission_date DESC
        LIMIT ?
    """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_export_data():
    """Returns all student results joined with demographic data for detailed export."""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            r.code, r.first_name, r.last_name, r.sex, r.college, r.year_attended_college as year_level,
            r.email_address, r.submission_date,
            p.phq9_result, p.gad7_result, p.sbqr_result
        FROM responses r
        LEFT JOIN predictions p ON r.code = p.code
        ORDER BY r.submission_date DESC
    """)
    
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def insert_feedback(student_code, data):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO counselor_feedback 
        (student_code, verified_phq9, verified_gad7, verified_sbqr, clinical_notes, timestamp)
        VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    """, (
        student_code, 
        data.get('verified_phq9'), 
        data.get('verified_gad7'), 
        data.get('verified_sbqr'), 
        data.get('clinical_notes')
    ))
    
    conn.commit()
    conn.close()

def fetch_feedback(student_code):
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM counselor_feedback WHERE student_code = ?", (student_code,))
    row = cursor.fetchone()
    
    conn.close()
    return dict(row) if row else None
