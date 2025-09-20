from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import KirimState
from db import add_transaction
from keyboard.reply import main_menu

kirim_router = Router()

@kirim_router.message(F.text == "➕ Kirim")
async def kirim_start(message: Message, state: FSMContext):
    await message.answer("💰 Qancha kirim bo'ldi? (faqat son yozing)")
    await state.set_state(KirimState.amount)

@kirim_router.message(KirimState.amount)
async def kirim_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("❗️ Iltimos, faqat son kiriting!")
    await state.update_data(amount=int(message.text))
    await message.answer("📝 Kirim uchun izoh kiriting (masalan: Oylik)")
    await state.set_state(KirimState.description)

@kirim_router.message(KirimState.description)
async def kirim_description(message: Message, state: FSMContext):
    data = await state.get_data()
    amount = data["amount"]
    description = message.text
    add_transaction(message.from_user.id, "kirim", amount, description)
    await message.answer("✅ Kirim muvaffaqiyatli saqlandi!", reply_markup=main_menu())
    await state.clear()
