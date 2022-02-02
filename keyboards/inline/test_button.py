from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from random import shuffle
def variantlar(correct,values,kategory):
    inline_keyboard = []
    while len(inline_keyboard)<2:
        word = values.pop(0)
        if word !=correct:
            inline_keyboard.append(word)
    inline_keyboard=[[InlineKeyboardButton(text=i,callback_data=f"notogri:{kategory}")] for i in inline_keyboard]
    inline_keyboard.append([InlineKeyboardButton(text=str(correct),callback_data=f"togri:{kategory}")])
    shuffle(inline_keyboard)       
    return InlineKeyboardMarkup(
        row_width=2,
        inline_keyboard=inline_keyboard
        
    )
