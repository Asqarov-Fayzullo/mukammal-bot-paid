import aiogram
from aiogram.types import CallbackQuery,Message
from aiogram.dispatcher import FSMContext
import asyncio
from data.config import ADMINS
from filters.admin import CallbackAdminFilter
from loader import dp,db,bot
from keyboards.inline.user_options import tasdiqlash,bolimlar

@dp.callback_query_handler(text="yangi_soz")
async def horijoy_sozni_sora(call:CallbackQuery,state:FSMContext):
    await call.answer()
    await state.set_state("horijiy_sozni_olish")
    user = await db.select_user(telegramID=call.message.chat.id)
    await call.message.edit_text(f"Ingliz tilidagi so'zni yuboring")

@dp.message_handler(content_types="text",state="horijiy_sozni_olish")
async def horijiy_sozni_olish(message:Message,state:FSMContext):
    await message.delete()
    word = await db.select_word(eng=message.text)
    if word:
        msg = await bot.edit_message_text(chat_id=message.from_user.id,message_id=message.message_id-1,text="Bu so'z bizda bor")
        await asyncio.sleep(2)
        await msg.delete()
        await message.answer("Bo'limlardan qiziqarlisini tanlang",reply_markup=bolimlar())
        await state.finish()
        return
    await state.update_data({'horijiy':message.text})
    await state.set_state("uzbekcha_sozni_olish")
    await bot.edit_message_text(chat_id=message.from_user.id,message_id=message.message_id-1,text="So'zni o'zbekchasini yuboring")


@dp.message_handler(content_types="text",state="uzbekcha_sozni_olish")
async def horijiy_sozni_olish(message:Message,state:FSMContext):
    await state.update_data({'uzbekcha':message.text})
    # # await state.set_state("tilni_olish")
    # await state.set_state("soz_turkumi")
    # data = await state.get_data()
    # # await message.answer(f"{data.get('horijiy')} qaysi tilda?",reply_markup=tillar_for_new_word())
    # await message.answer("So'z turkumini tanlang",reply_markup=soz_turkumlari())
    # user = await db.select_user(telegram_id=message.chat.id)
    data = await state.get_data()
    horijiy = data.get("horijiy")
    await state.set_state("tasdiqlash")
    await message.delete()
    try:
        await bot.edit_message_text(chat_id=message.from_user.id,message_id=message.message_id-2,text=f"{horijiy}=={message.text}?",reply_markup=tasdiqlash())
    except aiogram.utils.exceptions.MessageToEditNotFound:
        await message.answer(text=f"{horijiy}=={message.text}?",reply_markup=tasdiqlash())
# @dp.callback_query_handler(text=["rusadd","inglizadd"],state="tilni_olish")
# async def set_user_language(call:CallbackQuery,state:FSMContext):
#     await call.answer()
#     await state.update_data({'til':call.data.strip('add')})
#     await state.set_state("soz_turkumi")
#     await call.message.answer("So'z turkumini tanlang",reply_markup=soz_turkumlari())
    

# @dp.callback_query_handler(text=["Ot","Sifat","Son","Fel"],state="soz_turkumi")
# async def tastiqlash(call:CallbackQuery,state:FSMContext):
#     await call.answer()
#     # userstate = await state.get_state(default="Yoq" )
#     # await call.message.answer(f"State: {userstate}")
#     # user = await db.select_user(telegram_id=call.message.chat.id)
#     # data = await state.get_data()
#     # uzbekcha = data.get("uzbekcha")
#     # horijiy = data.get("horijiy")
#     # # til = data.get("til")
#     # await state.set_state("tasdiqlash")
#     # await call.message.delete()
#     # await call.message.answer(f"{horijiy}=={uzbekcha}?\nTil:{user.get('til')} tili\nso'z turkumi:{call.data}",reply_markup=tasdiqlash())

@dp.callback_query_handler(text="get_new_word_id")
async def get_new_word_id(call:CallbackQuery):
    word = call.message.text.split('\n')[0].split('-')[0]
    word_in_db = await db.select_word(eng=word)
    await call.message.answer(f"WordID:<code>{word_in_db.get('id')}</code>\nidni nusxalash uchun ustiga bosing")
    await call.message.answer("Bo'limlardan qiziqarlisini tanlang",reply_markup=bolimlar())