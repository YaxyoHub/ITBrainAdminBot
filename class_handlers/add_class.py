from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.class_db import add_class
from states import ClassForm
from keyboards.reply import class_menu
from keyboards.inline import teachers_inline

class_router = Router()

# ➕ Sinf qo‘shish
@class_router.message(F.text == "➕Sinf qo'shish")
async def add_class_start(message: Message, state: FSMContext):
    await message.answer("🏫 Yangi sinf nomini kiriting:")
    await state.set_state(ClassForm.name)


# Sinf nomi
@class_router.message(ClassForm.name)
async def add_class_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📖 Ushbu sinf uchun kurs nomini kiriting (masalan: Backend, Frontend):")
    await state.set_state(ClassForm.course)


# Kurs nomi
@class_router.message(ClassForm.course)
async def add_class_course(message: Message, state: FSMContext):
    await state.update_data(course=message.text)
    await message.answer("👨‍🏫 Ushbu sinfga o‘qituvchini tanlang:", reply_markup=teachers_inline())


# Inline teacher tanlash
@class_router.callback_query(F.data.startswith("teacher:"))
async def select_teacher(callback: CallbackQuery, state: FSMContext):
    teacher_name = callback.data.split(":")[1]
    await state.update_data(teacher=teacher_name)
    await callback.message.delete()
    await callback.message.answer("⏰ Dars vaqtini kiriting (masalan: 10:00-12:00):")
    await state.set_state(ClassForm.time)
    await callback.answer(f"O‘qituvchi tanlandi: {teacher_name}")


# Vaqt
@class_router.message(ClassForm.time)
async def add_class_time(message: Message, state: FSMContext):
    await state.update_data(time=message.text)
    data = await state.get_data()

    name = data["name"]
    course = data["course"]
    teacher = data["teacher"]
    time = data["time"]

    add_class(
        name,
        course,
        teacher,
        time
    )

    await message.answer(
        f"✅ Yangi sinf qo‘shildi:\n\n"
        f"🏫 Nomi: {name}\n"
        f"📖 Kurs: {course}\n"
        f"👨‍🏫 O‘qituvchi: {teacher}\n"
        f"⏰ Vaqti: {time}", reply_markup=class_menu
    )
    await state.clear()

