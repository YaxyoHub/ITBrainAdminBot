import asyncio, logging
import datetime
import sqlite3

from utils.throttling import ThrottlingMiddleware
from loader import dp, bot, menu_commands, admin_id
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.reply import menu

from database.pupil_db import init_pupils
from database.class_db import init_classes
from database.teacher_db import init_teachers
from db import statistik_db

from handlers.pupils import pupil_router
from class_handlers.classes import class_m 
from teacher_handlers.teacher import teacher_router
from statistic_handlers.payments import payment_router
from statistic_handlers.xarajat import xarajat_router
from handlers.error import error_router

DB_NAME = "school.db"


# === To‘lovlarni nol qilish funksiyasi ===
def reset_monthly_payments():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE pupils SET sum = 0;")
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Barcha o‘quvchilarning to‘lovlari 0 qilindi.")


# === Background task ===
async def monthly_reset_task():
    while True:
        now = datetime.datetime.now()
        if now.day == 1 and now.hour == 0 and now.minute == 0:
            reset_monthly_payments()
            await asyncio.sleep(60)  # 1 daqiqa kutish, qayta ishlamasligi uchun
        await asyncio.sleep(30)  # har 30 soniyada tekshiradi


@dp.message(Command('start'))
async def start_cmd(message: Message):
    if message.from_user.id != admin_id:
        return await message("⚠️<b>Ushbu faqat Admin uchun</b>\nOddiy foydalanuvchilar ishlatishi mumkin emas!")
    await message.answer(f"Salom {message.from_user.full_name} | IT Brain TC , Admin Menyusi:", reply_markup=menu)


@dp.message(F.text == "⬅️ Asosiy menyuga qaytish")
async def back_main_menu(message: Message):
    await message.answer("✅Asosiy menudasiz", reply_markup=menu)



# dp yaratgandan keyin
dp.message.middleware(ThrottlingMiddleware(rate_limit=0.5))  # 0.5 sekund


dp.include_router(pupil_router)
dp.include_router(class_m)
dp.include_router(teacher_router)
dp.include_router(payment_router)
dp.include_router(xarajat_router)

dp.include_router(error_router)



async def main():
    # 🔥 background task qo‘shamiz
    asyncio.create_task(monthly_reset_task())
    await menu_commands()
    await dp.start_polling(bot)


if __name__ == "__main__":
    statistik_db()
    init_pupils()
    init_classes()
    init_teachers()
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
