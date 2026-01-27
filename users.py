import sqlite3

DB_NAME = "expenses.db"

def create_users_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()


    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def create_user(email, password_hash):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (email, password) VALUES (?, ?)",
        (email, password_hash)
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return user_id


def get_user_by_email(email):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )
    user = cur.fetchone()
    conn.close()
    return user


def merge_temp_user(temp_id, real_user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(
        "UPDATE expenses SET user_id = ? WHERE user_id = ?",
        (real_user_id, temp_id)
    )
    conn.commit()
    conn.close()
