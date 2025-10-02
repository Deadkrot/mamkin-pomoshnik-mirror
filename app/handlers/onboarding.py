from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.orm import Session
from ..states import Onb
from ..models import User
from ..keyboards import main_kb
from ..services.age_rules import feeds_by_age_months

router = Router(name="onboarding")

@router.message(F.text == "/start")
async def start(m: Message, state: FSMContext, db: Session):
    u = db.query(User).filter(User.tg_id == m.from_user.id).first()
    if not u:
        u = User(tg_id=m.from_user.id)
        db.add(u); db.commit()
    if u.onboarding_done:
        await m.answer("С возвращением! Что делаем?", reply_markup=main_kb()); return
    await m.answer("Привет! Сколько месяцев малышу? (целое число)")
    await state.set_state(Onb.age_months)

@router.message(Onb.age_months)
async def set_age(m: Message, state: FSMContext, db: Session):
    try:
        age = int(m.text.strip())
        u = db.query(User).filter(User.tg_id == m.from_user.id).first()
        u.age_months = age
        u.feeds_per_day = feeds_by_age_months(age)
        db.commit()
        await m.answer(f"Ок. Рекомендуемых кормлений: {u.feeds_per_day}. Введите своё число или отправьте 'ok'.")
        await state.set_state(Onb.feeds_per_day)
    except:
        await m.answer("Введите число месяцев, например: 5")

@router.message(Onb.feeds_per_day)
async def set_feeds(m: Message, state: FSMContext, db: Session):
    u = db.query(User).filter(User.tg_id == m.from_user.id).first()
    txt = m.text.strip().lower()
    if txt != "ok":
        try:
            val = int(txt)
            if 3 <= val <= 10:
                u.feeds_per_day = val; db.commit()
            else:
                await m.answer("Введите число от 3 до 10 или 'ok'"); return
        except:
            await m.answer("Введите число или 'ok'"); return
    await m.answer("Во сколько подъём утром? (HH:MM, напр. 07:00)")
    await state.set_state(Onb.wake_time)

@router.message(Onb.wake_time)
async def set_wake(m: Message, state: FSMContext, db: Session):
    u = db.query(User).filter(User.tg_id == m.from_user.id).first()
    u.wake_time = m.text.strip(); db.commit()
    await m.answer("Когда начинается ночь? (HH:MM, напр. 20:30)")
    await state.set_state(Onb.night_start)

@router.message(Onb.night_start)
async def set_night_start(m: Message, state: FSMContext, db: Session):
    u = db.query(User).filter(User.tg_id == m.from_user.id).first()
    u.night_start = m.text.strip(); db.commit()
    await m.answer("Когда заканчивается ночь? (HH:MM, напр. 06:30)")
    await state.set_state(Onb.night_end)

@router.message(Onb.night_end)
async def set_night_end(m: Message, state: FSMContext, db: Session):
    u = db.query(User).filter(User.tg_id == m.from_user.id).first()
    u.night_end = m.text.strip(); db.commit()
    await m.answer("Какую смесь используете? (оставьте как есть или введите)")
    await state.set_state(Onb.formula)

@router.message(Onb.formula)
async def set_formula(m: Message, state: FSMContext, db: Session):
    u = db.query(User).filter(User.tg_id == m.from_user.id).first()
    if m.text.strip():
        u.formula_name = m.text.strip()
    u.onboarding_done = 1; db.commit()
    await state.clear()
    await m.answer("Готово! Жмите «План на сегодня» или фиксируйте факты.", reply_markup=main_kb())
