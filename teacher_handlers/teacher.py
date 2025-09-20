from aiogram import Router, F
from aiogram.types import Message

from .add_teacher import add_teacher_router
from .see_teacher import  see_teacher_router

from keyboards.reply import teacher_menu

teacher_router = Router()

@teacher_router.message(F.text == "👤O'qituvchilar")
async def teachers_menu_cmd(message: Message):
    await message.answer("O'qituvchilar bo'limi", reply_markup=teacher_menu)

teacher_router.include_router(add_teacher_router)
teacher_router.include_router(see_teacher_router)