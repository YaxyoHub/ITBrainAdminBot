from aiogram import Router, F
from aiogram.types import Message

from keyboard.reply import main_menu
from .kirim import kirim_router
from .chiqim import chiqim_router
from .statistik import statistika_router

xarajat_router = Router()

@xarajat_router.message(F.text == "📊 Xarajatlar")
async def xarajat_cmd(message: Message):
    await message.answer("Moliyaviy hisob botiga xush kelibsiz!", reply_markup=main_menu())

xarajat_router.include_router(kirim_router)
xarajat_router.include_router(chiqim_router)
xarajat_router.include_router(statistika_router)