from aiogram import Router,F
from aiogram.filters import Command
from aiogram.types import Message,ReplyKeyboardMarkup,KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import aiogram
router=Router()
def get_main_reply_keyboard():
    keyboard=ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Найти машину")],
            [KeyboardButton(text="📦 Мои подписки"),KeyboardButton(text="🔔 Настроить радар"),KeyboardButton(text="📊 Статистика рынка")]
        ],
        resize_keyboard=True
    )
    return keyboard

@router.message(Command("start"))
async def Start(message:Message):
    name= message.from_user.first_name
    await message.answer(f"Привет {name} \nЯ помогу тебе мониторить появление крутых тачек по локальному API.",reply_markup=get_main_reply_keyboard())
@router.message(F.text == "📦 Мои подписки")
async def Find(message:Message):
    await message.answer(f"Какую марка вам нужно?")

@router.message(F.text == "🔔 Настроить радар")
async def Find(message:Message):
    await message.answer(f"No signal")
@router.message(F.text == "📊 Статистика рынка")
async def Find(message:Message):
    await message.answer(f"No signal")