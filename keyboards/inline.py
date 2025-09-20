import sqlite3
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.pupil_db import get_pupils_by_class

def teachers_inline():
    conn = sqlite3.connect("school.db")
    cur = conn.cursor()
    cur.execute("SELECT full_name FROM teacher;")
    teachers = cur.fetchall()
    conn.close()

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=teacher[0], callback_data=f"teacher:{teacher[0]}")]
            for teacher in teachers
        ]
    )
    return keyboard

def pupils_inline(class_m):
    pupils_list = get_pupils_by_class(class_m)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"▪️{pupil[1]}", callback_data=f"pupil_:{pupil[1]}")]
            for pupil in pupils_list
        ]
    )
    return keyboard

def pupils_inline_payment(class_m):
    pupils_list = get_pupils_by_class(class_m)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"💳-> {pupil[1]}", callback_data=f"💳_:{pupil[1]}")]
            for pupil in pupils_list
        ]
    )
    return keyboard

back_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Ortga", callback_data="back_payment")]
    ]
)
