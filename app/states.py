from aiogram.fsm.state import StatesGroup, State

class Onb(StatesGroup):
    age_months = State()
    feeds_per_day = State()
    wake_time = State()
    night_start = State()
    night_end = State()
    formula = State()
