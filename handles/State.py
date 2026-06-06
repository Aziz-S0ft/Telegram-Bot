from aiogram.fsm.state import State, StatesGroup
class group(StatesGroup):
    brand=State()
    model=State()
    price=State()
class static(StatesGroup):
    choose=State()
    brand=State()
    model=State()