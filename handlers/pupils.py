from aiogram import Router, F
from aiogram.types import Message

from .add_pupil import add_pupil_router
from .see_and_delete import see_del_router

from keyboards.reply import pupil_menu

pupil_router = Router()

@pupil_router.message(F.text == "👤 O'quvchilar")
async def pupils_menu_cmd(message: Message):
    await message.answer("O'quvchilar bo'limi", reply_markup=pupil_menu)

pupil_router.include_router(add_pupil_router)
pupil_router.include_router(see_del_router)