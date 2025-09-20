from aiogram import Router, F
from aiogram.types import Message
from db import get_transactions, clear_transactions
from keyboard.reply import statistika_menu, clear_back, main_menu

statistika_router = Router()

@statistika_router.message(F.text == "📊 Statistika")
async def show_statistika(message: Message):
    await message.answer("📊 Qaysi hisobotni ko'rmoqchisiz?", reply_markup=statistika_menu())

@statistika_router.message(F.text == "📈 Kirim hisoboti")
async def kirim_report(message: Message):
    records = get_transactions(message.from_user.id, "kirim")
    if not records:
        return await message.answer("📭 Kirimlar hali yo'q.", reply_markup=clear_back())

    total = sum([r[1] for r in records])
    text = "\n\n".join([
        f"{i+1})\n📅 {r[0]}\n💰 {r[1]} so'm\n📝 {r[2]}"
        for i, r in enumerate(records)
    ])
    text += f"\n\n<b>Jami kirim:</b> {total} so'm"

    await message.answer(f"<b>Kirim hisoboti:</b>\n\n{text}", reply_markup=clear_back())


@statistika_router.message(F.text == "📉 Chiqim hisoboti")
async def chiqim_report(message: Message):
    records = get_transactions(message.from_user.id, "chiqim")
    if not records:
        return await message.answer("📭 Chiqimlar hali yo'q.", reply_markup=clear_back())

    total = sum([r[1] for r in records])
    text = "\n\n".join([
        f"{i+1})\n📅 {r[0]}\n💸 {r[1]} so'm\n📝 {r[2]}"
        for i, r in enumerate(records)
    ])
    text += f"\n\n<b>Jami chiqim:</b> {total} so'm"

    await message.answer(f"<b>Chiqim hisoboti:</b>\n\n{text}", reply_markup=clear_back())


@statistika_router.message(F.text == "🗑️ Tarixni tozalash")
async def clear_all(message: Message):
    if "Kirim" in message.text:
        clear_transactions(message.from_user.id, "kirim")
        await message.answer("🗑️ Kirimlar tozalandi!", reply_markup=clear_back())
    elif "Chiqim" in message.text:
        clear_transactions(message.from_user.id, "chiqim")
        await message.answer("🗑️ Chiqimlar tozalandi!", reply_markup=clear_back())
    else:
        # Har ikkisini tozalash
        clear_transactions(message.from_user.id, "kirim")
        clear_transactions(message.from_user.id, "chiqim")
        await message.answer("🗑️ Barcha tarix tozalandi!", reply_markup=clear_back())

@statistika_router.message(F.text == "🔙 Ortga")
async def back_to_statistika(message: Message):
    await message.answer("📊 Qaysi hisobotni ko'rmoqchisiz?", reply_markup=statistika_menu())

@statistika_router.message(F.text == "🔙 Menuga qaytish")
async def back_to_main(message: Message):
    await message.answer("🏠 Asosiy menyudasiz", reply_markup=main_menu())
