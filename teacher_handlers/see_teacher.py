from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.reply import teachers_keyboard, teacher_menu
from database.teacher_db import delete_teacher, get_teacher_by_name

see_teacher_router = Router()

@see_teacher_router.message(F.text == "📝O'qituvchilarni ko'rish")
async def see_teacher_cmd(message: Message):
    await message.answer(f"Marhamat O'quv markazdagi barcha sinflar", reply_markup=teachers_keyboard())
    
@see_teacher_router.message(F.text.startswith("teacher_"))
async def get_teacher_for_delete(message: Message):
    teacher_p = message.text.strip()[8:]  
    teacher_info = get_teacher_by_name(teacher_p)

    if not teacher_info:
        await message.answer("❌ Bunday o'qituvchi topilmadi.")
        return

    # unpack qilamiz
    id, full_name, phone_number, nickname, type, _ = teacher_info


    text = (
        f"👤 O'qituvchi: {full_name}\n"
        f"📞 Telefon raqami: {phone_number}\n"
        f"📱 Telegram: {nickname}\n"
        f"📚 Texnologiya: {type}\n\n"
    )

    # Inline tugmalar
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ O‘chirish", callback_data=f"Del_teacher{full_name}")],
            [InlineKeyboardButton(text="⬅️ Ortga", callback_data="Back_to_teachers")]
        ]
    )

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

@see_teacher_router.callback_query(F.data.startswith("Del_teacher"))
async def delete_teacher_cmd(callback: CallbackQuery):
    teacher_name = callback.data[11:]

    success = delete_teacher(teacher_name)

    if success:
        await callback.message.delete()
        await callback.message.answer(f"✅ {teacher_name}  muvaffaqiyatli o‘chirildi.", reply_markup=teachers_keyboard())
    else:
        await callback.message.delete()
        await callback.message.answer(f"❌ {teacher_name} ni o‘chirishda xatolik yuz berdi.", reply_markup=teachers_keyboard())

    await callback.answer()  # callback yuklanishini yopish

# ⬅️ Ortga tugmasi
@see_teacher_router.callback_query(F.data == "Back_to_teachers")
async def back_to_teacher(callback: CallbackQuery):
    # Barcha sinflarni qaytadan chiqaramiz
    await callback.message.delete()
    await callback.message.answer(
        "📚 Marhamat, o‘quv markazdagi barcha oq'ituvchilar:",
        reply_markup=teachers_keyboard()
    )
    await callback.answer()

@see_teacher_router.message(F.text == "⬅️ Ortga qaytish")
async def back_to_menu_teachers(message: Message):
    await message.answer("O'qituvchi menusi", reply_markup=teacher_menu)