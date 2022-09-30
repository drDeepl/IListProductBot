from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from models.week_model import week

from service.request import get_schedule, download_schedule
from service.convert_images import convert_pdf_to_image
from service.Messages import Message

from keyboards.create_keyboard import create_inline_keyboard
from keyboards.models import model_keyboard_menu


from states.Schedule import Schedule
from settings import TOKEN


bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'], state="*")
async def start_bot(message: types.Message, state=FSMContext):
        # TODO добавить редактирование сообщения, чтобы работать с одним сообщением
        current_state = await state.get_state()
        message_id = message.message_id
        bot_message = message_id + 1
        if current_state is not None:
                await state.finish()
        async with state.proxy() as data:
                data['start_message'] = message
                data["start_message_bot"] = bot_message        
        await Schedule.click_show_schedule.set()
        
        kb = create_inline_keyboard(week)
        
        await message.answer(text=Message.show_schedule, reply_markup=kb)

@dp.message_handler(state="*")
async def count_messages_take(message: types.Message, state: FSMContext):
        async with state.proxy() as data:
                data['count_messages'] += 1

@dp.callback_query_handler(lambda callback: "week" in callback.data, state=Schedule.click_show_schedule)
async def show_schedule(callback_query: types.callback_query, state=FSMContext):
        states: dict = await state.get_data()
        bot_message: int = states.get("start_message_bot")
        message_with_schedule: int = states.get("message_with_schedule")
        if message_with_schedule is None:
                message_with_schedule: int = bot_message + 1
        
        chat_id: int= callback_query.message.chat.id
        
        async with state.proxy() as data:
                data["message_with_schedule"] = message_with_schedule
        
        await bot.edit_message_text(text=Message.find_schedule,chat_id=chat_id,message_id=bot_message)
        try:
                list_schedule = get_schedule()
        except:
                await bot.send_message(chat_id=chat_id, text=Message.have_error)
        name_week = week[callback_query.data].lower()
        for item in list_schedule:
                callback_data_name_week = item.get("type").get("name").lower()
                if  callback_data_name_week == name_week:
                        url_to_pdf_file_schedule = item.get("attachments")[0].get("file")
                        download_schedule(url_to_pdf_file_schedule)
                        image_schedule = convert_pdf_to_image()
                        
                        kb_menu = create_inline_keyboard(model_keyboard_menu)
                        
                        
                        await bot.edit_message_reply_markup(chat_id=chat_id, message_id=bot_message, reply_markup=kb_menu)
                        await bot.send_photo(chat_id=chat_id, photo=image_schedule)
                        await Schedule.click_in_menu.set()
                        return

@dp.callback_query_handler(state=Schedule.click_in_menu)
async def prepare_init_state(callback_query: types.callback_query, state: FSMContext):
       # TODO: Вычислить сообщение бота после отправки нескольких сообщений от пользователея
        
        states: dict = await state.get_data()
        
        # count_messages: int = states.get("count_messages")
        message_id_with_schedule : int  = states.get("message_with_schedule")
        start_message_id = states.get("start_message_bot")
        chat_id = callback_query.message.chat.id
        kb = create_inline_keyboard(week)
        await bot.delete_message(chat_id=chat_id, message_id=message_id_with_schedule)
        async with state.proxy() as data:
                data["message_with_schedule"] = message_id_with_schedule + 1
                data["count_messages"] = 0
        await Schedule.click_show_schedule.set()
        await bot.edit_message_text(text=Message.show_schedule, chat_id=chat_id, message_id=start_message_id, reply_markup=kb)
        
