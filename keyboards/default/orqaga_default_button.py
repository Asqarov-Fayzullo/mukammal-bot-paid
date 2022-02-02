from aiogram.types import ReplyKeyboardMarkup,KeyboardButton

def default_orqaga():
    markup=ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Orqaga")
            ]
        ],
        resize_keyboard=True,
    )
    return markup