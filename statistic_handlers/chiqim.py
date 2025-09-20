from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states import ChiqimState
from db import add_transaction
from keyboard.reply import main_menu

chiqim_router = Router()

@chiqim_router.message(F.text == "➖ Chiqim")
async def chiqim_start(message: Message, state: FSMContext):
    await message.answer("💸 Qancha chiqim bo'ldi? (so'mda)")
    await state.set_state(ChiqimState.amount)

@chiqim_router.message(ChiqimState.amount)
async def chiqim_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("❗️ Iltimos, faqat son kiriting!")
    await state.update_data(amount=int(message.text))
    await message.answer("📝 Chiqim uchun izoh kiriting (masalan: Nonushta)")
    await state.set_state(ChiqimState.description)

@chiqim_router.message(ChiqimState.description)
async def chiqim_description(message: Message, state: FSMContext):
    data = await state.get_data()
    amount = data["amount"]
    description = message.text
    add_transaction(message.from_user.id, "chiqim", amount, description)
    await message.answer("✅ Chiqim muvaffaqiyatli saqlandi!", reply_markup=main_menu())
    await state.clear()
