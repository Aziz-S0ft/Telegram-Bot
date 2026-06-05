from aiogram import Router,F
from aiogram.filters import Command
from aiogram.types import Message,ReplyKeyboardMarkup,KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from datebase.sql_select import init_first_db,init_second_db,add_users
from handles.Findcar import get_main_reply_keyboard
import aiogram
router=Router()
@router.message(Command("start"))
async def Start(message:Message):
    await init_first_db()  #исползвал один раз
    await init_second_db() 
    name= message.from_user.first_name
    ID=message.from_user.id
    await add_users(ID,name)
    await message.answer(f"Привет {name} \nЯ помогу тебе мониторить появление крутых тачек по локальному API.",reply_markup=get_main_reply_keyboard())
@router.message(F.text == "Найти машину")
async def Find(message:Message):
    await message.answer(f"Какую марка вам нужно?")
@router.message(F.text == "📦 Мои подписки")
async def Find(message:Message):
    await message.answer(f"No signal")
@router.message(F.text == "🔔 Настроить радар")
async def Find(message:Message):
    await message.answer(f"No signal")
@router.message(F.text == "📊 Статистика рынка")
async def Find(message:Message):
    await message.answer(f"No signal")