print("✅ MY storage.py LOADED")

import sqlite3
from datetime import date

DB_NAME = "expenses.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def get_daily_total(user_id):
    conn = get_connection()
    cur = conn.cursor()

    today = date.today().isoformat()  # '2026-01-28'

    cur.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM expenses
        WHERE user_id = ?
        AND date = ?
    """, (user_id, today))

    total = cur.fetchone()[0]
    conn.close()
    return total

# ================= TABLE =================

def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT,
            category TEXT,
            amount REAL,
            description TEXT
        )
    """)

    conn.commit()
    conn.close()


# ================= CREATE =================

def add_expense(expense):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO expenses (user_id, date, category, amount, description)
        VALUES (?, ?, ?, ?, ?)
    """, (
        expense.user_id,
        expense.date,
        expense.category,
        expense.amount,
        expense.description
    ))

    conn.commit()
    conn.close()


# ================= READ =================

def get_expenses_by_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM expenses
        WHERE user_id = ?
        ORDER BY date DESC
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()
    return rows


def get_expense_by_id_and_user(expense_id, user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM expenses
        WHERE id = ? AND user_id = ?
    """, (expense_id, user_id))

    expense = cur.fetchone()
    conn.close()
    return expense


# ================= UPDATE =================

def update_expense(expense_id, user_id, date, category, amount, description):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE expenses
        SET date = ?, category = ?, amount = ?, description = ?
        WHERE id = ? AND user_id = ?
    """, (
        date,
        category,
        amount,
        description,
        expense_id,
        user_id
    ))

    conn.commit()
    conn.close()


# ================= DELETE =================

def delete_expense(expense_id, user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM expenses WHERE id = ? AND user_id = ?",
        (expense_id, user_id)
    )

    conn.commit()
    conn.close()



# ================= AGGREGATES =================

def get_category_totals_by_user(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT category, SUM(amount) AS total
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
    """, (user_id,))

    rows = cur.fetchall()
    conn.close()
    return rows


def get_total_by_type_and_user(summary_type, value, user_id):
    conn = get_connection()
    cur = conn.cursor()

    if summary_type == "daily":
        cur.execute("""
            SELECT SUM(amount)
            FROM expenses
            WHERE date = ? AND user_id = ?
        """, (value, user_id))

    elif summary_type == "monthly":
        cur.execute("""
            SELECT SUM(amount)
            FROM expenses
            WHERE substr(date,1,7) = ? AND user_id = ?
        """, (value, user_id))

    elif summary_type == "yearly":
        cur.execute("""
            SELECT SUM(amount)
            FROM expenses
            WHERE substr(date,1,4) = ? AND user_id = ?
        """, (value, user_id))

    total = cur.fetchone()[0]
    conn.close()
    return total or 0
