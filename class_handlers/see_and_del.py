from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.pupil_db import get_count
from database.class_db import get_class_by_name, delete_class
from keyboards.reply import classes_keyboard, class_menu

delete_router = Router()

@delete_router.message(F.text == "📝Sinflarni ko'rish")
async def see_del_cmd(message: Message):
    await message.answer(f"Marhamat O'quv markazdagi barcha sinflar", reply_markup=classes_keyboard())
    
@delete_router.message(F.text.startswith("Class_"))
async def get_class_for_delete(message: Message):
    class_p = message.text.strip()[6:]  # "class_7A" -> "7A"
    class_info = get_class_by_name(class_p)

    if not class_info:
        await message.answer("❌ Bunday sinf topilmadi.")
        return

    # unpack qilamiz
    id, name, type_, teacher_name, time, pupils = class_info

    # O‘quvchilar ro‘yxatini ko‘rkam chiqarish

    text = (
        f"🏫 <b>Sinf nomi:</b> {name}\n"
        f"📚 <b>Turi:</b> {type_}\n"
        f"👨‍🏫 <b>O‘qituvchi:</b> {teacher_name}\n"
        f"⏰ <b>Vaqt:</b> {time}\n\n"
    )

    # Inline tugmalar
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ O‘chirish", callback_data=f"Del_class{name}")],
            [InlineKeyboardButton(text="⬅️ Ortga", callback_data="Back_to_classes")]
        ]
    )

    await message.answer(text, reply_markup=keyboard, parse_mode="HTML")

@delete_router.callback_query(F.data.startswith("Del_class"))
async def delete_class_cmd(callback: CallbackQuery):
    print("Callback data:", callback.data)  # 👈 aynan nima kelayotganini ko‘ramiz
    class_name = callback.data[9:]  # Del_class → uzunligi 9
    print("Kesilgan class_name:", class_name)

    success = delete_class(class_name)

    if success:
        await callback.message.delete()
        await callback.message.answer(f"✅ {class_name} sinfi muvaffaqiyatli o‘chirildi.", reply_markup=classes_keyboard())
    else:
        await callback.message.delete()
        await callback.message.answer(f"❌ {class_name} sinfini o‘chirishda xatolik yuz berdi.", reply_markup=classes_keyboard())

    await callback.answer()  # callback yuklanishini yopish

# ⬅️ Ortga tugmasi
@delete_router.callback_query(F.data == "Back_to_classes")
async def back_to_classes(callback: CallbackQuery):
    # Barcha sinflarni qaytadan chiqaramiz
    await callback.message.delete()
    await callback.message.answer(
        "📚 Marhamat, o‘quv markazdagi barcha sinflar:",
        reply_markup=classes_keyboard()
    )
    await callback.answer()

@delete_router.message(F.text == "⬅️ Ortga")
async def back_to_menu_classes(message: Message):
    await message.answer("Sinf menusi", reply_markup=class_menu)