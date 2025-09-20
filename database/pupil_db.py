import sqlite3

DB_NAME = 'school.db'

class init_pupils():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pupils (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT,
                phone_number TEXT,
                course_type TEXT,
                class_n TEXT,
                sum INTEGER DEFAULT 0
                );
    """)
    conn.commit()
    cur.close()
    conn.close()

def add_user(name, phone, course, class_n):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO pupils (full_name, phone_number, course_type, class_n)
                VALUES (?, ?, ?, ?);
    """, (name, phone, course, class_n,))
    conn.commit()
    cur.close()
    conn.close()

def get_count():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM pupils;")
    data = cur.fetchone()[0]   # faqat bitta son qaytadi
    cur.close()
    conn.close()
    return data

def get_pupils_by_class(class_n):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM pupils WHERE class_n = ?;", (class_n,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_pupil_by_name(name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM pupils WHERE full_name = ?;", (name,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data


def delete_pupil(name: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM pupils WHERE full_name = ?;", (name,))
        conn.commit()
        return True   # ❌ rowcount emas, to‘g‘ridan-to‘g‘ri True qaytaramiz
    except Exception as e:
        print("Xatolik:", e)
        return False
    finally:
        conn.close()

### Payment ### 


def get_pupils_by_class(class_n):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, full_name, phone_number, course_type, class_n, sum FROM pupils WHERE class_n = ?;", (class_n,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data  # list of tuples


def get_pupil_by_id(pupil_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT id, full_name, phone_number, course_type, class_n, sum FROM pupils WHERE id = ?;", (pupil_id,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data  # tuple or None


def payment_pupil(pupil_id: int, amount: int) -> bool:
    """
    amount — integer (masalan 100000)
    Bu funksiya mavjud `sum` ustuniga amount ni qo'shib yozadi.
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        # avval hozirgi sum ni o'qiymiz
        cur.execute("SELECT sum FROM pupils WHERE id = ?;", (pupil_id,))
        row = cur.fetchone()
        if not row:
            cur.close()
            conn.close()
            return False  # bunday id yo'q

        current = row[0] or 0
        new_sum = int(current) + int(amount)

        cur.execute("UPDATE pupils SET sum = ? WHERE id = ?;", (new_sum, pupil_id))
        conn.commit()
        cur.close()
        conn.close()
        return True

    except Exception as e:
        print("payment_pupil error:", e)
        try:
            conn.close()
        except:
            pass
        return False   # ✅ endi to‘g‘ri joylashdi



### Payment ### 

import datetime

DB_NAME = "school.db"

def reset_monthly_payments():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Agar jadvalda ustun bo'lmasa, qo'shamiz
    cur.execute("""
    CREATE TABLE IF NOT EXISTS meta (
        key TEXT PRIMARY KEY,
        value TEXT
    );
    """)

    # Oxirgi reset sanasini olish
    cur.execute("SELECT value FROM meta WHERE key = 'last_reset_month';")
    row = cur.fetchone()

    current_month = datetime.datetime.now().strftime("%Y-%m")  # Masalan: 2025-09

    if row is None:
        # Birinchi marta bo'lsa, yozib qo'yamiz
        cur.execute("INSERT INTO meta (key, value) VALUES (?, ?)", ("last_reset_month", current_month))
    else:
        last_reset_month = row[0]
        if last_reset_month != current_month:
            # Agar yangi oy bo'lsa, barcha o'quvchilarning summasini 0 qilamiz
            cur.execute("UPDATE pupils SET sum = 0;")
            # Meta jadvalni yangilaymiz
            cur.execute("UPDATE meta SET value = ? WHERE key = 'last_reset_month';", (current_month,))
            print("✅ Har oylik reset bajarildi.")
        else:
            print("⏳ Bu oy allaqachon reset qilingan.")

    conn.commit()
    cur.close()
    conn.close()