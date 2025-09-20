import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

load_dotenv()

admin_id = int(os.getenv('ADMIN'))

bot_token = os.getenv("API_TOKEN")
bot = Bot(token=bot_token, default=DefaultBotProperties(parse_mode='HTML'))

dp = Dispatcher()

from aiogram.types import BotCommand, BotCommandScopeDefault

async def menu_commands():
    commands = [
        BotCommand(command='start', description='Botni ishga tushirish uchun')
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())