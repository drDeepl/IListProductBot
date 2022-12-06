
from aiogram.dispatcher.filters.state import State, StatesGroup

class ListProduct(StatesGroup):
    add_product = State()
    show_products = State()
