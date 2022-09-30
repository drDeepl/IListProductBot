from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    ReplyKeyboardMarkup, 
    KeyboardButton)





def create_inline_keyboard(data_keyboard: dict) -> InlineKeyboardMarkup:
    if type(data_keyboard) is dict:
        kb = InlineKeyboardMarkup()
        for callback_data in data_keyboard.keys():
            text = data_keyboard[callback_data]
            kb_button = InlineKeyboardButton(text=text, callback_data=callback_data,)
            kb.add(kb_button)

        return kb
    else:
        raise TypeError("data_keyboard must be dict")


