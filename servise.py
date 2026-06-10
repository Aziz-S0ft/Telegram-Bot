from aiogram import Bot
from datebase.sql_select import find_cars
from dotenv import load_dotenv
import os
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
async def send_message(data:dict):
    global bot
    sell_cars='Привет у нас вышло такой вариант!\n'
    sell_cars+=f"{data['brand']} {data['model']} {data['engine']} \nГод выпуска:{data['year']} \nЦена:{data['price_usd']}\nОписание:{data['description']}"
    photos_url=data['photo_url']
    info=await find_cars(data['brand'],data['model'])
    for key,value in info.items():
        if value<data['price_usd']:continue
        await bot.send_photo(
            chat_id=key,
            photo=photos_url,
            caption=sell_cars
        )