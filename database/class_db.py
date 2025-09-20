import sqlite3

DB_NAME = 'school.db'

class init_classes():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                type TEXT,
                teacher_name TEXT,
                time TEXT,
                name_pupils TEXT
                );
    """)
    conn.commit()
    cur.close()
    conn.close()


def add_class(name, type, teacher, time):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO classes (name, type, teacher_name, time)
                VALUES (?, ?, ?, ?);
    """, (name, type, teacher, time))
    conn.commit()
    cur.close()
    conn.close()


def add_pupil_class(pupil, name_class):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Eski o‘quvchilar ro‘yxatini olish
    cur.execute("SELECT name_pupils FROM classes WHERE name = ?", (name_class,))
    result = cur.fetchone()
    if result and result[0]:
        pupils = result[0].split(",")  # eski ro‘yxatni massivga aylantirish
    else:
        pupils = []

    # Yangi o‘quvchini qo‘shish
    pupils.append(pupil)
    new_pupils = ",".join(pupils)

    # Yangilash
    cur.execute("UPDATE classes SET name_pupils = ? WHERE name = ?", (new_pupils, name_class))
    conn.commit()
    conn.close()

def get_classes():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM classes;
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def get_class_by_name(name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    SELECT * FROM classes WHERE name = ?;
    """, (name,))
    data = cur.fetchone()
    cur.close()
    conn.close()
    return data

def delete_class(name: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM classes WHERE name = ?", (name,))
        conn.commit()
        return True   # ❌ rowcount emas, to‘g‘ridan-to‘g‘ri True qaytaramiz
    except Exception as e:
        print("Xatolik:", e)
        return False
    finally:
        conn.close()


