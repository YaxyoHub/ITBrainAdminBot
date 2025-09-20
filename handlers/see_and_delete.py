from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.pupil_db import get_count, get_pupil_by_name, delete_pupil
from database.class_db import get_class_by_name
from keyboards.reply import classes_keyboard_2, pupil_menu
from keyboards.inline import pupils_inline

see_del_router = Router()

@see_del_router.message(F.text == "📝O'quvchilarni ko'rish")
async def see_pupil_cmd(message: Message):
    await message.answer(f"O'quv markazda {get_count()} ta o'quvchi bor\n"
                         "Ko'proq ma'lumot uchun sinflar orqali topib, ma'lumot oling", reply_markup=classes_keyboard_2())
    
@see_del_router.message(F.text.startswith("class_"))
async def get_pupil_for_delete(message: Message):
    class_p = message.text.strip()[6:]  # "class_7A" -> "7A"
    class_info = get_class_by_name(class_p)

    if not class_info:
        await message.answer("❌ Bunday sinf topilmadi.")
        return

    # sinfdagi o‘quvchilarni olib kelamiz
    keyboard = pupils_inline(class_p)

    if not keyboard.inline_keyboard:  # inline tugmalar bo'sh bo'lsa
        await message.answer(f"❌ '{class_p}' sinfida o‘quvchilar yo‘q.", reply_markup=classes_keyboard_2())
        return

    await message.answer(f"👥 Marhamat {class_p} sinfidagi o‘quvchilar:", reply_markup=keyboard)


@see_del_router.callback_query(F.data.startswith("pupil_:"))
async def del_pupil_cmd(callback: CallbackQuery):
    pupil_m = callback.data[7:]
    pupil_data = get_pupil_by_name(pupil_m)
    await callback.message.delete()
    
    id, name, phone_number, course_type, class_n, _ = pupil_data

    text = (f"O'quvchi ma'lumotlari\n\n"
    f"👤 To'liq ismi: {name}\n"
    f"📞 Telefon raqami: {phone_number}\n"
    f"📚 Yunalishi: {course_type}\n"
    f"🏛 Sinf: {class_n}\n")

    # Inline tugmalar
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ O‘chirish", callback_data=f"del_pupil:{name}")],
            [InlineKeyboardButton(text="⬅️ Ortga", callback_data="back_to_pupils")]
        ]
    )

    await callback.message.answer(text, reply_markup=keyboard, parse_mode="HTML")

@see_del_router.callback_query(F.data.startswith("del_pupil:"))
async def delete_class_cmd(callback: CallbackQuery):
    pupil_name = callback.data[10:]  

    success = delete_pupil(pupil_name)

    if success:
        await callback.message.delete()
        await callback.message.answer(f"✅ {pupil_name} muvaffaqiyatli o‘chirildi.", reply_markup=classes_keyboard_2())
    else:
        await callback.message.delete()
        await callback.message.answer(f"❌ {pupil_name} ni o‘chirishda xatolik yuz berdi.", reply_markup=classes_keyboard_2())

    await callback.answer()  # callback yuklanishini yopish

# ⬅️ Ortga tugmasi
@see_del_router.callback_query(F.data == "back_to_pupils")
async def back_to_classes(callback: CallbackQuery):
    # Barcha sinflarni qaytadan chiqaramiz
    await callback.message.delete()
    await callback.message.answer(
        "📚 Marhamat, o‘quv markazdagi barcha sinflar:",
        reply_markup=classes_keyboard_2()
    )
    await callback.answer()

@see_del_router.message(F.text == "⬅️ Orqaga")
async def back_to_menu_classes(message: Message):
    await message.answer("O'quvchilar menusi", reply_markup=pupil_menu)
