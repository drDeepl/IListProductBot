from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from database.Products import Products,initialize_db, db_close
from service.Messages import Message

from keyboards.create_keyboard import create_inline_keyboard


from models.models_keyboard import start_menu

from states.ListProducts import ListProduct
from settings import TOKEN


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'], state="*")
async def show_schedule(message: types.Message, state=FSMContext):
       kb = create_inline_keyboard(start_menu)
       await message.answer(text="Вот моё меню", reply_markup=kb)

@dp.callback_query_handler(lambda callback: "add_product" in callback.data)
async def show_schedule(callback_query: types.callback_query, state=FSMContext):
        await ListProduct.add_product.set()
        chat_id: int = callback_query.message.chat.id
        await bot.send_message(chat_id=chat_id, text="Отправь мне название продукта")

@dp.message_handler(state=ListProduct.add_product)
async def show_schedule(message: types.Message, state=FSMContext):
        product = message.text
        chat_id = message.chat.id
        try:
                Products.create(name=product)
                
        except Exception:
                db_close()
                initialize_db()
                
                
                        
        await state.finish()
        await bot.send_message(chat_id=chat_id, text="Готово!")



@dp.callback_query_handler(lambda callback: "list_products" in callback.data)
async def prepare_init_state(callback_query: types.callback_query, state: FSMContext):
        chat_id = callback_query.message.chat.id
        res = ""
        products = Products.select()
        for product in products:
                
                res += product.name + "\n"
        await bot.send_message(chat_id=chat_id, text=f"Твой список покупок:\n {res}")

        
