from aiogram import Router,F
from aiogram.filters import Command
from aiogram.types import Message,ReplyKeyboardMarkup,KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from datebase.sql_select import init_first_db,init_second_db,add_users,add_ann,select_sub,del_sub
from handles import Findcar
from handles.State import group,static,delete_car
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
    await message.answer(f"Какую марка вам нужно?\nЕсли хотите отменит нажмите /channel",reply_markup=Findcar.get_car_brand_keyboard().as_markup(resize_keyboard=True))
    await state.set_state(group.brand)
@router.message(Command("channel"))
async def Channel(message:Message,state:FSMContext):
    await state.clear()
    await message.answer("Вы успешно отменили!")
@router.message(group.brand)
async def Brand(message:Message,state=FSMContext):
    if not message.text in list(Findcar.bran_model.keys()):
        return
    await state.update_data(brand=message.text)
    await message.answer(f"Какую модель вам нужно?\nЕсли хотите отменит нажмите /channel",reply_markup=Findcar.get_car_model_keyboard(message.text).as_markup(resize_keyboard=True))
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
    await message.answer(f"Какой ваш бюджет?\nЕсли хотите отменит нажмите /channel")
    await state.set_state(group.price)
@router.message(group.price)
async def price(message:Message,state:FSMContext):
    ID=message.from_user.id
    if not message.text.isdigit():
        await message.answer("Пишите только цифры!")
        return
    data= await state.get_data()
    model=data.get("model")
    brand=data.get("brand")
    price=int(message.text)
    await state.clear()
    await add_ann(ID,brand,model,price)
    await message.answer(f"Вы выбрали {brand} {model} \nВаш бюджет:{price}")
    cars_info,images=Findcar.info_from_cars(brand,model,price)
    if cars_info:
        await message.answer("Мы нашли такие варианты\n")
        for i in zip(cars_info,images):
            await message.answer_photo(i[1],caption=i[0])
    else:await message.answer('Мы не нашли хорошие варианты')


@router.message(F.text == "📦 Мои подписки")
async def sub(message:Message):
    subs = await select_sub(message.from_user.id)
    if not subs:
        await message.answer("У вас пока нет активных подписок.")
    else:
        text = "Ваши подписки:\n"
        for brand, model, price in subs:
            text += f"🚗 {brand} {model} — за {price} $\n"
        await message.answer(text)
@router.message(F.text == "🔔 Настроить радар")
async def delete_sub(message:Message,state:FSMContext):
    await state.set_state(delete_car.which)
    subs = await select_sub(message.from_user.id)
    if not subs:
        await message.answer("У вас пока нет активных подписок.")
    else:
        await message.answer("Какую вы хотите удалить?",reply_markup=Findcar.build_sub(subs).as_markup(resize_keyboard=True))
@router.message(delete_car.which)
async def which_sub(message:Message,state:FSMContext):
    subs = await select_sub(message.from_user.id)
    if Findcar.prov_del_sub(subs,message.text):
        await message.answer("Успешно удаленно!")
        sub_chose=message.text.split(sep='  ')
        user_id=message.from_user.id
        await del_sub(user_id,sub_chose[1],sub_chose[2],sub_chose[5])
        await state.clear()
    else :
        await message.answer("Извените такой подписка не нашлось")
        return
@router.message(F.text == "📊 Статистика рынка")
async def stat(message:Message,state:FSMContext):
    await message.answer("Выберите один из них!", reply_markup=Findcar.get_cars_info_keyboard().as_markup(resize_keyboard=True))
    await state.set_state(static.choose)
@router.message(static.choose)
async def chos(message:Message,state:FSMContext):
    if message.text=="Общие цифры рынка":
        pass
    elif message.text=="Статистика по брендам (Топ-3 на нашей площадке)":
        top_3b=Findcar.top_brands()
        await message.answer(f"Топ 1 бренд:{top_3b[0]} \nTоп 2 бренд:{top_3b[1]}\nТоп 3 бренд:{top_3b[2]}")
        await state.clear()
    elif message.text=="Средняя цена по конкретным моделям (Для фанатов)":
        await state.update_data(car=True)
        await state.set_state(static.brand)
        await message.answer(f"Какую марка вам нужно?\nЕсли хотите отменит нажмите /channel",reply_markup=Findcar.get_car_brand_keyboard().as_markup(resize_keyboard=True))
    else:return
@router.message(static.brand)
async def brand(message:Message,state:FSMContext):
    if not message.text in list(Findcar.bran_model.keys()):
        return
    await state.update_data(brand=message.text)
    await message.answer(f"Какую модель вам нужно?\nЕсли хотите отменит нажмите /channel",reply_markup=Findcar.get_car_model_keyboard(message.text).as_markup(resize_keyboard=True))
    await state.set_state(static.model)
@router.message(static.model)
async def Model(message:Message,state:FSMContext):
    data= await state.get_data()
    model=message.text
    brand=data.get("brand")
    if Findcar.proverka(brand,model):
        return
    avr=Findcar.avr_car(brand,model)
    await state.clear()
    await message.answer(f"{brand} {model} среднем продается за:{avr}")
