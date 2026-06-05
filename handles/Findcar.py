from aiogram.types import Message,ReplyKeyboardMarkup,KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
def get_main_reply_keyboard():
    keyboard=ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Найти машину")],
            [KeyboardButton(text="📦 Мои подписки"),KeyboardButton(text="🔔 Настроить радар"),KeyboardButton(text="📊 Статистика рынка")]
        ],
        resize_keyboard=True
    )
    return keyboard
def get_car_brand_keyboard():
    brands=ReplyKeyboardBuilder()
    brands.add(KeyboardButton(text=""))