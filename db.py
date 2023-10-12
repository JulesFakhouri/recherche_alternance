import sqlite3

def create_database():
    conn = sqlite3.connect('job_search.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_type TEXT,
            status TEXT,
            date DATE,
            company_name TEXT,
            job_title TEXT,
            job_link TEXT,
            job_text TEXT
        )
    ''')

    conn.commit()
    return conn

def insert_job_entry(conn, job_type, status, date, company_name, job_title, job_link, job_text):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO job_entries (job_type, status, date, company_name, job_title, job_link, job_text) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (job_type, status, date, company_name, job_title, job_link, job_text))
    conn.commit()

def fetch_all_job_entries(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_entries")
    return cursor.fetchall()

def fetch_filtered_job_entries(conn, job_type, status, company_name):
    query = "SELECT * FROM job_entries WHERE 1"
    params = []

    if job_type != "Tous":
        query += " AND job_type = ?"
        params.append(job_type)

    if status != "Tous":
        query += " AND status = ?"
        params.append(status)

    if company_name:
        query += " AND company_name LIKE ?"
        params.append(f"%{company_name}%")

    cursor = conn.cursor()
    cursor.execute(query, params)
    return cursor.fetchall()
