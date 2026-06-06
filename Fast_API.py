from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import json
api= FastAPI(title="Car Marketplace API")
class Cars_sell_info(BaseModel):
    id: int 
    brand:str
    model:str
    year:int
    price_usd:int
    engine:str
    description:str
    photo_url:str

@api.post("/app/sellcars")
def create_api(sub:Cars_sell_info):
    return {
        "status": "success", 
        "message": "API added successfully",
        "data": sub
    }
with open ("data.json","r",encoding="utf-8") as f:
    sellcars=json.load(f)
@api.get("/app/sellcars")
def info_cars():
    return sellcars
@api.get("/app/sellcars/{id_cars}")
def info_car(id_cars:int):
    if id_cars >len(sellcars):
        raise HTTPException(status_code=404,detail="Нету такой машина!")
    return sellcars[id_cars-1]