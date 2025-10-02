from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session
from ..models import User, Event
from ..utils_time import now_tz

router = Router(name="facts")

@router.callback_query(F.data == "feed_now")
async def feed_now(cb: CallbackQuery, db: Session):
    u = db.query(User).filter(User.tg_id == cb.from_user.id).first()
    if not u:
        await cb.answer(); return
    t = now_tz(u.tz)
    db.add(Event(tg_id=u.tg_id, kind="feed", at=t, note=None)); db.commit()
    await cb.message.answer(f"🍼 Зафиксировано кормление: {t.strftime('%H:%M')}. Подстрою следующий интервал.")
    await cb.answer()

@router.callback_query(F.data == "sleep_start")
async def sleep_start(cb: CallbackQuery, db: Session):
    u = db.query(User).filter(User.tg_id == cb.from_user.id).first()
    if not u:
        await cb.answer(); return
    t = now_tz(u.tz)
    db.add(Event(tg_id=u.tg_id, kind="sleep_start", at=t, note=None)); db.commit()
    await cb.message.answer(f"😴 Сон начат: {t.strftime('%H:%M')}.")
    await cb.answer()

@router.callback_query(F.data == "sleep_end")
async def sleep_end(cb: CallbackQuery, db: Session):
    u = db.query(User).filter(User.tg_id == cb.from_user.id).first()
    if not u:
        await cb.answer(); return
    t = now_tz(u.tz)
    db.add(Event(tg_id=u.tg_id, kind="sleep_end", at=t, note=None)); db.commit()
    await cb.message.answer(f"😊 Пробуждение: {t.strftime('%H:%M')}. После сна пора поесть.")
    await cb.answer()
