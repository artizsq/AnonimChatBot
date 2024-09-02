from aiogram.filters import BaseFilter
from data.requests import get_chat, create_chat, get_queue, add_queue, delete_queue, delete_chat
import asyncio

class IsChat(BaseFilter):
    async def __call__(self, message):
        chat = await get_chat(message.from_user.id)
        if chat:
            return True
        return False