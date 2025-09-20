import sqlite3

DB_NAME = 'school.db'

class init_teachers():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS teacher (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                phone_number TEXT,
                nickname TEXT,
                type TEXT,
                classes TEXT
                );
    """)
    conn.commit()
    cur.close()
    conn.close()


def add_teacher(name, phone, tg, type):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO teacher (full_name, phone_number, nickname, type)
                VALUES (?, ?, ?, ?);
    """, (name, phone, tg, type))
    conn.commit()
    cur.close()
    conn.close()

def delete_teacher(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM teacher WHERE full_name = ?", (name,))
        conn.commit()
        return True   # ❌ rowcount emas, to‘g‘ridan-to‘g‘ri True qaytaramiz
    except Exception as e:
        print("Xatolik:", e)
        return False
    finally:
        conn.close()

def get_teachers():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM teacher;
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_teacher_by_name(name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM teacher WHERE full_name = ?;
    """, (name,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data

