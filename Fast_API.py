from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from servise import send_message
import json
api= FastAPI(title="Car Marketplace API")
class Cars_sell_info(BaseModel):
    id: int | None = None
    brand:str
    model:str
    year:int
    price_usd:int
    engine:str
    description:str
    photo_url:str
    created_at:str = Field(
        default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    )

with open ("data.json","r",encoding="utf-8") as f:
    sellcars:list=json.load(f)
@api.get("/app/sellcars")
async def info_cars():
    return sellcars
@api.get("/app/sellcars/{id_cars}")
async def info_car(id_cars:int):
    if id_cars >len(sellcars):
        raise HTTPException(status_code=404,detail="Нету такой машина!")
    return sellcars[id_cars-1]
@api.post("/app/sellcars")
async def add_car(car:Cars_sell_info):
    new_car_data=car.model_dump()
    new_car_data['id']=len(sellcars)+1
    sellcars.append(new_car_data)
    with open('data.json','w',encoding='utf-8') as f:
        json.dump(sellcars,f,ensure_ascii=False,indent=4)
    await send_message(new_car_data)
    return {'hello':'state'}