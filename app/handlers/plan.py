from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.orm import Session
from datetime import datetime
from ..models import User
from ..services.planner import plan_day
from ..utils_time import now_tz

router = Router(name="plan")

@router.callback_query(F.data == "plan_today")
async def show_plan(cb: CallbackQuery, db: Session):
    u = db.query(User).filter(User.tg_id == cb.from_user.id).first()
    if not u or not u.onboarding_done:
        await cb.message.answer("Сначала пройдите /start")
        return
    day_now = now_tz(u.tz)
    plan = plan_day(day_now, u.age_months or 3, u.feeds_per_day, u.wake_time, u.night_start, u.night_end)
    feeds = "\n".join(f"🍼 {t.strftime('%H:%M')}" for t,_ in plan["feeds"])
    naps = "\n".join(f"😴 {s.strftime('%H:%M')}–{e.strftime('%H:%M')}" for s,e in plan["naps"])
    text = f"*План на сегодня*\nКормления:\n{feeds}\n\nСны:\n{naps}"
    await cb.message.answer(text, parse_mode="Markdown")
    await cb.answer()
