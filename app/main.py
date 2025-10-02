import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Update

from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from .config import BOT_TOKEN
from .db import init_db, SessionLocal
from .scheduler import start_scheduler
from .handlers.onboarding import router as onboarding_router
from .handlers.plan import router as plan_router
from .handlers.facts import router as facts_router

class SessionMiddleware:
    def __init__(self, session_factory):
        self.session_factory = session_factory
    async def __call__(self, handler, event: Update, data: dict):
        db: Session = self.session_factory()
        try:
            data["db"] = db
            return await handler(event, data)
        finally:
            db.close()

async def main():
    if not BOT_TOKEN:
        raise SystemExit("BOT_TOKEN is not set. Put it into .env")
    init_db()
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.outer_middleware(SessionMiddleware(SessionLocal))
    dp.include_router(onboarding_router)
    dp.include_router(plan_router)
    dp.include_router(facts_router)
    start_scheduler()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
