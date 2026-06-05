from aiogram.types import Message,ReplyKeyboardMarkup,KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import json
def get_main_reply_keyboard():
    keyboard=ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Найти машину")],
            [KeyboardButton(text="📦 Мои подписки"),KeyboardButton(text="🔔 Настроить радар"),KeyboardButton(text="📊 Статистика рынка")]
        ],
        resize_keyboard=True
    )
    return keyboard
with open ("data.json","r",encoding="utf-8" ) as f :
    data = json.load(f)
bran_model={}

for i in data:
    if not i["brand"] in bran_model:
        bran_model[i["brand"]]=set()
        bran_model[i["brand"]].add(i["model"])
    else:
        bran_model[i["brand"]].add(i["model"])
def get_car_brand_keyboard():
    brands=ReplyKeyboardBuilder()
    for i in bran_model.keys():
        brands.add(KeyboardButton(text=i))
    brands.adjust(3)
    return brands
def get_car_model_keyboard(brand):
    models=ReplyKeyboardBuilder()
    for i in bran_model[brand]:
        models.add(KeyboardButton(text=i))
    models.adjust(3)
    return models
def proverka(brand,model):
    if model in bran_model.get(brand, set()): return False
    else:return True