from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
import aiogram
router=Router()
@router.message(Command("start"))
async def Start(message:Message):
    await message.answer("Hello")