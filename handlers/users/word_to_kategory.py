from aiogram.types import CallbackQuery,Message,ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
import asyncpg
from keyboards.default.orqaga_default_button import default_orqaga
from keyboards.inline.user_options import manage_kategory,user_word_categories
from loader import dp,db,bot


@dp.callback_query_handler(lambda c:str(c.data).startswith("add_word_to_kategory"),state="kategory_manager")
async def get_word_for_kategory(call:CallbackQuery,state:FSMContext):
    # print(f"calldata{call.data}")
    await state.update_data({'kategory_id':call.data.split(':')[1]})
    await call.answer()
    await state.set_state("soz_id_olish")
    await call.message.answer(text="Yangi so'zni yuboring",reply_markup=default_orqaga())
    await call.message.delete()

@dp.message_handler(content_types="text",state="soz_id_olish")
async def get_word_id(message:Message,state:FSMContext):
    data = await state.get_data()
    if message.text == "Orqaga":
        await state.set_state("kategories")
        user=await db.select_user(telegramID=message.chat.id)
        user_kategory_ids=user.get('categorylistid')
        if user_kategory_ids:
            user_kategories = [await db.select_category(i) for i in user_kategory_ids]
        else:
            user_kategories=[]
        m=await message.answer(text="😝",reply_markup=ReplyKeyboardRemove())
        await m.delete()
        return await message.answer("Kategoriyalar",reply_markup=user_word_categories(categorylist=user_kategories))
    if not message.text.isalpha():
        return await message.answer("So'zda raqamlar qatnashmasin")
    word = await db.select_word(eng=message.text)
    if word:
        if await db.insert_kategory_word(kategoryID=int(data.get('kategory_id')),word_id=int(word.get('id')))==0:
            await message.answer("Bu so'z kategoriyada bor boshqa so'z yuboring")
            return
        await message.answer(f"So'z kategoriyaga qo'shildi\n{word.get('eng')} - {word.get('uz')}\nkeyingi sozni yuboring")
    else:
        await message.answer("Bu so'z botda majud emas botga so'zni qo'shish uchun sizni yangi so'z qo'shish bo'limiga yo'naltiramiz")
        await message.answer("So'zni o'zbekchasini yuboring",reply_markup=ReplyKeyboardRemove())
        await state.set_state("uzbekcha_sozni_olish")
        await state.update_data({'horijiy':message.text})


