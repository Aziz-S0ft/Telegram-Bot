from aiogram import Router,F
from aiogram.filters import Command
from aiogram.types import Message,ReplyKeyboardMarkup,KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from datebase.sql_select import init_first_db,init_second_db,add_users
from handles import Findcar
from handles.State import group
import aiogram
router=Router()
@router.message(Command("start"))
async def Start(message:Message):
    #await init_first_db()  #исползвал один раз
    #await init_second_db() 
    name= message.from_user.first_name
    ID=message.from_user.id
    await add_users(ID,name)
    await message.answer(f"Привет {name} \nЯ помогу тебе мониторить появление крутых тачек по локальному API.",reply_markup=Findcar.get_main_reply_keyboard())
@router.message(F.text == "Найти машину")
async def Find(message:Message,state=FSMContext):
    await message.answer(f"Какую марка вам нужно?",reply_markup=Findcar.get_car_brand_keyboard().as_markup(resize_keyboard=True))
    await state.set_state(group.brand)
@router.message(group.brand)
async def Brand(message:Message,state=FSMContext):
    if not message.text in list(Findcar.bran_model.keys()):
        return
    await state.update_data(brand=message.text)
    await message.answer(f"Какую модель вам нужно?",reply_markup=Findcar.get_car_model_keyboard(message.text).as_markup(resize_keyboard=True))
    await state.set_state(group.model)
@router.message(group.model)
async def Model(message:Message,state:FSMContext):
    data= await state.get_data()
    model=message.text
    brand=data.get("brand")
    if Findcar.proverka(brand,model):
        return
    print("i am here")
    await state.update_data(model=message.text)
    await message.answer(f"Какой ваш бюджет?")
    await state.set_state(group.price)
@router.message(group.price)
async def Model(message:Message,state:FSMContext):
    if not message.text.isdigit():
        return
    data= await state.get_data()
    model=data.get("model")
    brand=data.get("brand")
    price=int(message.text)
    await state.clear()
    await message.answer(f"Вы выбрали {brand} {model} \nВаш бюджет:{price}")
@router.message(F.text == "📦 Мои подписки")
async def Find(message:Message):
    await message.answer(f"No signal")
@router.message(F.text == "🔔 Настроить радар")
async def Find(message:Message):
    await message.answer(f"No signal")
@router.message(F.text == "📊 Статистика рынка")
async def Find(message:Message):
    await message.answer(f"No signal")