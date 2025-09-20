# utils/throttling.py
import time
from aiogram import BaseMiddleware
from aiogram.types import Message


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 1.0):
        """
        rate_limit - necha soniyada bitta xabar qabul qilinadi
        default: 1 sekund
        """
        super().__init__()
        self.rate_limit = rate_limit
        self.last_time = {}

    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id
        now = time.time()

        # oxirgi yuborilgan vaqtni tekshiramiz
        last = self.last_time.get(user_id, 0)
        if now - last < self.rate_limit:
            await event.answer("⏳ Iltimos, biroz kutib yuboring (spam yo‘q).")
            return  # handler ishlamaydi

        # vaqtni yangilash
        self.last_time[user_id] = now
        return await handler(event, data)
