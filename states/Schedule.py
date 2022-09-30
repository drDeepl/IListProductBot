
from aiogram.dispatcher.filters.state import State, StatesGroup

class Schedule(StatesGroup):
    click_show_schedule = State()
    click_in_menu = State()
