from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import asyncpg

from loader import dp,db
from keyboards.inline.user_options import bolimlar
from keyboards.default.orqaga_default_button import default_orqaga

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        await db.addNew_user(fullName=message.from_user.full_name,userName=message.from_user.username,telegramID=message.from_user.id)
    except asyncpg.exceptions.UniqueViolationError:
        pass
    await message.answer("Assalomu aleykum. Bo'limlardan qiziqarlisini tanlang",reply_markup=bolimlar())
    await message.delete()
