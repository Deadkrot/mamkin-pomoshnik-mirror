from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from aiogram import Bot
from sqlalchemy.orm import Session
from .models import Job

scheduler = AsyncIOScheduler()

async def schedule_once(bot: Bot, db: Session, tg_id: int, when: datetime, text: str, key: str):
    exists = db.query(Job).filter(Job.tg_id==tg_id, Job.key==key).first()
    if exists: return
    async def _job_send():
        try:
            await bot.send_message(tg_id, text)
        except Exception:
            pass
    scheduler.add_job(_job_send, DateTrigger(run_date=when))
    db.add(Job(tg_id=tg_id, key=key, when=when, payload=text))
    db.commit()

def start_scheduler():
    scheduler.start()
