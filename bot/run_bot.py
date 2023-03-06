import asyncio
from aiogram import Bot, Dispatcher
import settings
from bot import handlers


bot = Bot(token=settings.token)
dp = Dispatcher()


async def main():
    dp.include_router(handlers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

