from aiogram import Router, F
from aiogram.types import Message

from .add_class import class_router
from .see_and_del import delete_router

from keyboards.reply import class_menu

class_m= Router()

@class_m.message(F.text == "📝Sinflar")
async def classes_menu_cmd(message: Message):
    await message.answer("Sinflar bo'limi", reply_markup=class_menu)

class_m.include_router(class_router)
class_m.include_router(delete_router)