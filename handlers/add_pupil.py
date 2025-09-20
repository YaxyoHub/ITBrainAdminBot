from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import PupilForm
from database.pupil_db import add_user
from keyboards.reply import classes_keyboard_add, pupil_menu

add_pupil_router = Router()

@add_pupil_router.message(F.text == "➕O'quvchi qo'shish")
async def add_pupil_cmd(message: Message, state: FSMContext):
    await message.answer("Yangi o'quvchini to'liq ismini kiriting")
    await state.set_state(PupilForm.fullname)

# 👤 Ism
@add_pupil_router.message(PupilForm.fullname)
async def pupil_fullname(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer("📞 Telefon raqamini kiriting:")
    await state.set_state(PupilForm.phone)

# 📞 Telefon
@add_pupil_router.message(PupilForm.phone)
async def pupil_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("📚 Kurs turini kiriting (masalan: Backend, Frontend):")
    await state.set_state(PupilForm.course)

# 📚 Kurs turi
@add_pupil_router.message(PupilForm.course)
async def pupil_course(message: Message, state: FSMContext):
    await state.update_data(course=message.text)
    await message.answer("🏫 Qaysi sinfda o‘qishini kiriting (masalan: 7-A):", reply_markup=classes_keyboard_add())
    await state.set_state(PupilForm.class_name)

# 🏫 Sinf nomi
@add_pupil_router.message(PupilForm.class_name)
async def pupil_class(message: Message, state: FSMContext):
    await state.update_data(class_name=message.text)

    # ✅ Barcha ma’lumotlarni olish
    data = await state.get_data()
    fullname = data['fullname']
    phone = data['phone']
    course = data['course']
    class_name = data['class_name']

    add_user(
        fullname,
        phone,
        course,
        class_name
    )
    # 📌 Xabar
    await message.answer(
        f"✅ O‘quvchi qo‘shildi:\n\n"
        f"👤 Ism: {fullname}\n"
        f"📞 Telefon: {phone}\n"
        f"📚 Kurs: {course}\n"
        f"🏫 Sinf: {class_name}", reply_markup=pupil_menu
    )

    # 🔚 State tugatish
    await state.clear()
