from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from database.pupil_db import get_pupils_by_class, get_pupil_by_id, payment_pupil
from keyboards.reply import classes_keyboard_payment
from keyboards.inline import back_inline
from states import PaymentForm 

payment_router = Router()

# 1) Boshlash: sinfni so'rash
@payment_router.message(F.text == "💳 To'lovlar")
async def payment_cmd(message: Message):
    await message.answer("Qaysi sinf uchun to'lov qilmoqchisiz?", reply_markup=classes_keyboard_payment())

# 2) Sinf tanlandi -> sinfdagi o'quvchilar ro'yxatini message sifatida yuborish va id so'rash
@payment_router.message(F.text.startswith("💳_")) 
async def get_class_payment(message: Message, state: FSMContext):
    class_p = message.text.strip()[2:]
    pupils = get_pupils_by_class(class_p)

    if not pupils:
        await message.answer("❌ Ushbu sinfda o'quvchilar topilmadi.")
        return

    # formatlangan matn yaratish
    text_lines = ["""Qaysi o'quvchi to'lov qilmoqchisiz
    id       Ism         Summa
                  """]
    for i, row in enumerate(pupils, start=1):
        pid = row[0]
        name = row[1]
        curr_sum = row[5] or 0
        sum_text = f"{curr_sum} UZS" if int(curr_sum) != 0 else "0"
        text_lines.append(f"{i}) {pid} | {name} | {sum_text}")

    text_lines.append("\n<i>To'lov qilmoqchi bo'lgan o'quvchi idsini kiriting</i>")
    await message.answer("\n".join(text_lines), parse_mode="HTML", reply_markup=back_inline)

    # saqlab qo'yamiz qaysi sinf ekanligi, keyin id tekshiradi
    await state.update_data(selected_class=class_p)
    await state.set_state(PaymentForm.choose_id)

# 3) ID qabul qilish
@payment_router.message(PaymentForm.choose_id)
async def receive_pupil_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ Iltimos faqat raqam (o'quvchi id) kiriting.")
        return

    pupil_id = int(message.text.strip())
    pupil = get_pupil_by_id(pupil_id)
    if not pupil:
        await message.answer("❌ Bunday id li o'quvchi topilmadi. Qaytadan id kiriting.")
        return

    # hammasi ok — saqlab keyingi bosqichga o'tish
    await state.update_data(pupil_id=pupil_id)
    await message.answer(f"{pupil[1]} uchun qancha miqdorda to'lov qilmoqchisiz? (faqat raqam kiriting, misol: 100000)")
    await state.set_state(PaymentForm.sum)

# 4) Sum qabul qilish va saqlash
@payment_router.message(PaymentForm.sum)
async def receive_sum(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ Iltimos faqat raqam kiriting (masalan: 100000).")
        return

    data = await state.get_data()
    pupil_id = data.get('pupil_id')
    if not pupil_id:
        await message.answer("Xatolik: o'quvchi tanlanmagan. Iltimos boshidan boshlang.")
        await state.clear()
        return

    amount = int(message.text.strip())

    success = payment_pupil(pupil_id, amount)
    if not success:
        await message.answer("❌ To'lovni saqlashda xatolik yuz berdi.")
        await state.clear()
        return

    # tasdiq xabari
    pupil = get_pupil_by_id(pupil_id)
    new_sum = pupil[5] or 0
    await message.answer(f"✅ {pupil[1]} ga {amount} UZS to’lov qabul qilindi.\nJami to‘langan: {new_sum} UZS")

    # Yangilangan sinf ro'yxatini ko'rsatish (agar class saqlangan bo'lsa)
    selected_class = data.get('selected_class')
    if selected_class:
        pupils = get_pupils_by_class(selected_class)
        text_lines = [f"Yangilangan ro'yxat ({selected_class}):\n"]
        for i, row in enumerate(pupils, start=1):
            pid = row[0]
            name = row[1]
            curr_sum = row[5] or 0
            sum_text = f"{curr_sum} UZS" if int(curr_sum) != 0 else "0"
            text_lines.append(f"{i}) {pid} | {name} | {sum_text}")

        # ❗ oxiriga qo‘shamiz
        text_lines.append("\n<i>To‘lov qilmoqchi bo‘lgan o‘quvchi IDsini kiriting</i>")

        await message.answer("\n".join(text_lines), reply_markup=back_inline)

    await state.clear()


@payment_router.callback_query(F.data == "back_payment")
async def back_to_payment_cmd(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer("Qaysi sinfga to'lov qilmoqchisiz", reply_markup=classes_keyboard_payment())
    await callback.answer()