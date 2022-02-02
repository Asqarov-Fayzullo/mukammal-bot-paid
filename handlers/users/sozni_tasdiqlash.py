import asyncio
from aiogram.types import CallbackQuery,Message
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from filters.admin import CallbackAdminFilter
from loader import dp,db,bot
from keyboards.inline.user_options import tasdiqlash,get_new_word_id,bolimlar

@dp.callback_query_handler(text="togri:",state="tasdiqlash")
async def admin_tasdiqlashi(call:CallbackQuery,state:FSMContext):
    await call.answer()
    msg = await call.message.edit_text("Adminga yuborildi adminlarimiz so'zni tekshirishganidan so'ng sizga habar beramiz")
    await bot.send_message(ADMINS[0],text=f"Foydalanuvchi: <a href='tg://user?id={call.message.chat.id}'>{call.message.chat.full_name}</a>\n{call.message.text}",reply_markup=tasdiqlash(call.message.chat.id))
    await call.message.answer("Bo'limlardan qiziqarlisini tanlang",reply_markup=bolimlar())
    await state.finish()
    await asyncio.sleep(2)
    await msg.delete()

@dp.callback_query_handler(text="notogri:",state="tasdiqlash")
async def admin_tasdiqlashi(call:CallbackQuery,state:FSMContext):
    await call.answer()
    msg = await call.message.edit_text("Bekor qilindi")
    await call.message.answer("Bo'limlardan qiziqarlisini tanlang",reply_markup=bolimlar())
    await state.finish()
    await asyncio.sleep(2)
    await msg.delete()

@dp.callback_query_handler(CallbackAdminFilter(),lambda call: str(call.data).startswith("togri"))
async def admin_tasdiqlashi(call:CallbackQuery):
    await call.answer()
    await bot.send_message(chat_id=call.data.split(":")[1],text=call.message.text.replace('?','').replace('==','-')+'\n'+"Tasdiqladi bu so'zni o'z kategoriyangizga qo'shishingiz mumkin",
    # reply_markup=get_new_word_id()
    )
    # await bot.send_message(chat_id=call.data.split(':')[1],text="Tasdiqlandi id uchun tugmani bosing")
    eng,uz=call.message.text.split('\n')[1].replace('?','').split("==")
    turi=call.message.text.split('\n')[2].split(':')[1]
    await db.add_word(uz=uz,eng=eng,turi=turi)
    await bot.send_message(chat_id=call.data.split(":")[1],text="Bo'limlardan qiziqarlisini tanlang",reply_markup=bolimlar())


@dp.callback_query_handler(CallbackAdminFilter(),lambda call: str(call.data).startswith("notogri"))
async def admin_tasdiqlashi(call:CallbackQuery):
    await call.message.delete()
    msg = await bot.send_message(chat_id=call.data.split(":")[1],text=call.message.text.replace(call.message.text.split('\n')[0],'').replace('?','').replace('==','-')+'\n'+"Adminlar bekor qildi")
    await bot.send_message(chat_id=call.data.split(":")[1],text="Bo'limlardan qiziqarlisini tanlang",reply_markup=bolimlar())
    await asyncio.sleep(2)
    await msg.delete()