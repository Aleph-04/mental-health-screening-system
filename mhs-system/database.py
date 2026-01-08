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

            sbq1 INTEGER,
            sbq2 INTEGER,
            sbq3 INTEGER,
            sbq4 INTEGER,
            sbq_total INTEGER,
            sbq_risk TEXT
        )
    ''')

    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            college TEXT,
            age TEXT,
            phq9_result TEXT,
            gad7_result TEXT
        )
    ''')

    print("Hello from database.py")
    conn.close()


def insert_to_responses(first_name, middle_name, last_name, email_address,
                        phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
                        gad1, gad2, gad3, gad4, gad5, gad6, gad7,
                        sbq1, sbq2, sbq3, sbq4, sbq_total, sbq_risk):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO responses (
            first_name, middle_name, last_name, email_address,
            phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
            gad1, gad2, gad3, gad4, gad5, gad6, gad7,
            sbq1, sbq2, sbq3, sbq4, sbq_total, sbq_risk
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        first_name, middle_name, last_name, email_address,
        phq1, phq2, phq3, phq4, phq5, phq6, phq7, phq8, phq9,
        gad1, gad2, gad3, gad4, gad5, gad6, gad7,
        sbq1, sbq2, sbq3, sbq4, sbq_total, sbq_risk
    ))

    conn.commit()
    conn.close()
    print("Inserted response for", first_name)


def insert_to_predictions(name, college, age, phq9_prediction, gad7_prediction):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            name, college, age, phq9_result, gad7_result
        ) VALUES (?,?,?,?,?)
    """, (name, college, age, phq9_prediction, gad7_prediction))
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
    return [dict(row) for row in rows]


def count_records():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM responses")
    count = cursor.fetchone()[0]

    conn.close()
    return count
