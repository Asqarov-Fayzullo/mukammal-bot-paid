from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from keyboards.inline.user_options import bolimlar,user_word_categories
from loader import dp,db

@dp.callback_query_handler(text="categories")
async def categories(call:CallbackQuery,state:FSMContext):
    await call.answer()
    await state.set_state("kategories")
    user=await db.select_user(telegramID=call.message.chat.id)
    user_category_ids=user.get('categorylistid')
    user_categories=[]
    if user_category_ids:
        user_categories = [await db.select_category(i) for i in user_category_ids]
    await call.message.edit_text("Kategoriyalar",reply_markup=user_word_categories(categorylist=user_categories))