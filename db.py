# database.py
import sqlite3
from datetime import datetime

DB_NAME = "school.db"

def statistik_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Foydalanuvchilar jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE
    )
    """)

    # Kirim-chiqim jadvali
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        type TEXT,  -- 'kirim' yoki 'chiqim'
        amount INTEGER,
        description TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()

def add_user(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def get_user_count():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    return cursor.fetchone()[0]

def add_transaction(user_id: int, trans_type: str, amount: int, description: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (user_id, type, amount, description, date)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, trans_type, amount, description, datetime.now().strftime("%Y-%m-%d")))
    conn.commit()
    conn.close()

def get_transactions(user_id: int, trans_type: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, amount, description
        FROM transactions
        WHERE user_id = ? AND type = ?
        ORDER BY date DESC
    """, (user_id, trans_type))
    result = cursor.fetchall()
    conn.close()
    return result

def clear_transactions(user_id: int, trans_type: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM transactions WHERE user_id = ? AND type = ?", (user_id, trans_type))
    conn.commit()
    conn.close()

def get_user_transactions_summary(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT date, amount, comment, type FROM transactions 
        WHERE user_id = ? ORDER BY date ASC
    """, (user_id,))
    transactions = cursor.fetchall()

    summary = {
        "kirim": [],
        "chiqim": [],
        "jami_kirim": 0,
        "jami_chiqim": 0
    }

    for date, amount, comment, t_type in transactions:
        text = f"{date}\n{amount:,} so'm\n{comment}"
        if t_type == "kirim":
            summary["kirim"].append(text)
            summary["jami_kirim"] += amount
        elif t_type == "chiqim":
            summary["chiqim"].append(text)
            summary["jami_chiqim"] += amount

    return summary

