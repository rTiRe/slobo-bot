from aiogram.fsm.state import StatesGroup, State

class PublicBusket(StatesGroup):
    showing_random = State()
    showing_popular = State()