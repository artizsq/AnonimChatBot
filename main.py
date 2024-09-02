from aiogram import Bot, Dispatcher, types
import asyncio
from bot_code import rt
from data.models import async_main
import logging 

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token="")
    dp = Dispatcher()
    await async_main()

    dp.include_router(rt)

    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())