from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗓 План на сегодня", callback_data="plan_today")],
        [
            InlineKeyboardButton(text="🍼 Кормление сейчас", callback_data="feed_now"),
            InlineKeyboardButton(text="😴 Заснул", callback_data="sleep_start"),
            InlineKeyboardButton(text="😊 Проснулся", callback_data="sleep_end"),
        ],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")],
    ])
