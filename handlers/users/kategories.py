from telnetlib import NEW_ENVIRON
from aiogram.types import CallbackQuery,Message,ContentTypes
from aiogram.dispatcher import FSMContext
from keyboards.inline.user_options import user_word_categories,bolimlar,manage_kategory
from loader import dp,db,bot

@dp.callback_query_handler(text="orqaga",state="kategories")
async def orqaga(call:CallbackQuery,state:FSMContext):
    await call.answer()
    await state.finish()
    await call.message.edit_text("Bo'limlardan qiziqarlisini tanlang",reply_markup=bolimlar())

@dp.callback_query_handler(state="kategories",text="add_kategory")
async def add_kategory(call:CallbackQuery,state:FSMContext):
    await call.answer()
    await state.set_state("kategory_name")
    await state.update_data({'messageid':call.message.message_id,'message_markup':call.message.reply_markup,'chatid':call.message.chat.id})
    await call.message.answer("Kategoriyaga nom bering")

@dp.message_handler(content_types="text",state="kategory_name")
async def get_kategory_name(message:Message,state:FSMContext):
    
    new_kategory = await db.insert_new_kategory(title=message.text,userID=message.from_user.id)
    await db.insert_user_category(telegramID=message.from_user.id,categoryID=new_kategory.get('id'))
    data = await state.get_data()
    await state.set_state("kategories")
    user=await db.select_user(telegramID=message.from_user.id)
    user_category_ids=user.get('categorylistid')
    user_categories=[]
    if user_category_ids:
        user_categories = [await db.select_category(categoryID=i) for i in user_category_ids]
    markup = user_word_categories(categorylist=user_categories)
    
    # markup = data.get('message_markup').add(InlineKeyboardButton(text=message.text,callback_data=str(uuid4())))
    await bot.edit_message_reply_markup(reply_markup=markup,message_id=data.get('messageid'),chat_id=data.get('chatid'))
    await bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
    await bot.delete_message(chat_id=message.chat.id,message_id=message.message_id-1)

@dp.callback_query_handler(lambda c:str(c.data).startswith("iskategory"),state="kategories")
async def category_manager(call:CallbackQuery,state:FSMContext):
    await call.answer()
    await state.set_state("kategory_manager")
    kategory = await db.select_category(categoryID=int(call.data.split('-')[1]))
    await call.message.edit_text(text=f"Kategoriya: {kategory.get('title')}",reply_markup=manage_kategory(kategory.get('id')))
    

@dp.callback_query_handler(state="kategory_manager",text="kategories_statega_qaytish")
async def kategories_statega_qaytish(call:CallbackQuery,state:FSMContext):
    await call.answer()
    await state.set_state("kategories")
    user=await db.select_user(telegramID=call.message.chat.id)
    user_category_ids=user.get('categorylistid')
    if user_category_ids:
        user_categories = [await db.select_category(categoryID=i) for i in user_category_ids]
    else:
        user_categories=[]
    await call.message.edit_text(text="Categoriyalar",reply_markup=user_word_categories(categorylist=user_categories))
    


@dp.callback_query_handler(lambda c:str(c.data).startswith("kategory_words:"),state="kategory_manager")
async def see_kategory_words(call:CallbackQuery,state:FSMContext):
    category = await db.select_category(categoryID=int(call.data.split(':')[1]))
    word_ids = category.get('word_id_list')
    if not word_ids:
        return await call.message.answer("Kategoriyada so'zlar mavjud emas")
    words = [await db.select_word(id=int(i)) for i in word_ids]
    
    eng_words = [i.get('eng') for i in words]
    key = max(eng_words,key=len)
    message_text = "sizning so'zlar\n"
    for i in words:
        eng=i.get('eng')
        uz=i.get('uz')
        message_text+=f"{eng}{' '*((len(key)+3)-len(eng))} - {uz}\n"
    await call.message.answer(message_text)


@dp.callback_query_handler(lambda c:str(c.data).startswith("delete_kategory:"),state="kategory_manager")
async def delete_kategory(call:CallbackQuery,state:FSMContext):
    await db.delete_kategory(int(call.data.split(':')[1]),int(call.message.chat.id))
    await state.set_state("kategories")
    user=await db.select_user(telegramID=call.message.chat.id)
    user_category_ids=user.get('kategorylistid')
    user_categories=[]
    if user_category_ids:
        user_categories = [await db.select_category(categoryID=i) for i in user_category_ids]
    markup = user_word_categories(categorylist=user_categories)
    await call.message.edit_text(text="Kategoriyalar",reply_markup=markup)
