from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import TeacherForm
from database.teacher_db import add_teacher
from keyboards.reply import teacher_menu

add_teacher_router = Router()


@add_teacher_router.message(F.text == "➕O'qituvchi qo'shish")
async def add_teacher_cmd(message: Message, state: FSMContext):
    await message.answer("Yangi o'qituvchini to'liq ismini kiriting")
    await state.set_state(TeacherForm.name)

# 👤 Ism
@add_teacher_router.message(TeacherForm.name)
async def teacher_fullname(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("📞 Telefon raqamini kiriting:")
    await state.set_state(TeacherForm.phone)

# 📞 Telefon
@add_teacher_router.message(TeacherForm.phone)
async def teacher_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("O'qituvchining telegram username'ini yozing (Agar bulmasa Yo'q deb yozing)")
    await state.set_state(TeacherForm.nickname)

@add_teacher_router.message(TeacherForm.nickname)
async def teacher_nickname(message: Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await message.answer("📚 O'qituvchining yunalishini kiriting (masalan: Backend, Frontend):")
    await state.set_state(TeacherForm.type_m)

# 📚 Kurs turi
@add_teacher_router.message(TeacherForm.type_m)
async def teacher_course(message: Message, state: FSMContext):
    await state.update_data(type_m=message.text)

    # ✅ Barcha ma’lumotlarni olish
    data = await state.get_data()
    fullname = data['name']
    phone = data['phone']
    nickname = data['nickname']
    type_m = data['type_m']

    add_teacher(
        fullname,
        phone,
        nickname,
        type_m
    )
    # 📌 Xabar
    await message.answer(
        f"✅ O‘quvchi qo‘shildi:\n\n"
        f"👤 Ism: {fullname}\n"
        f"📱 Telegram: {nickname}"
        f"📞 Telefon: {phone}\n"
        f"📚 Kurs: {type_m}\n", reply_markup=teacher_menu
    )

    # 🔚 State tugatish
    await state.clear()
