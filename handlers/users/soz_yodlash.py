from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
import asyncio
from keyboards.inline.user_options import user_word_categories, bolimlar
from keyboards.inline.test_button import variantlar
from loader import dp, db, bot


@dp.callback_query_handler(text="soz_yodlash")
async def soz_yodlashga_kirish(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state('yodlash_uchun_kategoriya')
    user = await db.select_user(telegramID=call.message.chat.id)
    user_category_ids = user.get('kategory_id_list')
    user_categories = []
    if user_category_ids:
        user_categories = [await db.select_category(categoryID=i) for i in user_category_ids]
    await call.message.edit_text("Qaysi kategoriyadagi sozlarni yodlamoqchisiz", reply_markup=user_word_categories(categorylist=user_categories, key="soz_yodlash"))


@dp.callback_query_handler(text="orqagasoz_yodlash", state="yodlash_uchun_kategoriya")
async def oqaga_bolimlarga(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("Bo'limlardan qiziqarlisini tanlang", reply_markup=bolimlar())


@dp.callback_query_handler(lambda c: str(c.data).startswith("iskategory-soz_yodlash"), state="yodlash_uchun_kategoriya")
async def kategory_manager(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state("soz_yodlash")
    kategory = await db.select_category(int(call.data.split('soz_yodlash')[1]))
    words = []
    for i in kategory.get('word_id_list'):
        words.append(await db.select_word(id=int(i)))
    worddict = {}
    for i in words:
        worddict[i.get('eng')] = i.get('uz')
    if len(worddict) < 3:
        msg = await call.message.answer("Kategoriyaga kamida 4ta so'z qo'shing")
        await call.message.delete()
        await call.message.answer("Bo'limlardan qiziqarlisini tanlang", reply_markup=bolimlar())
        await state.finish()
        return
    msg = await call.message.edit_text(f"Kategoriya: {kategory.get('name')}")
    await asyncio.sleep(2)
    await msg.edit_text("Tayyormisiz")
    await asyncio.sleep(2)
    await msg.edit_text("Kettik")
    await asyncio.sleep(2)
    # await msg.delete()
    await call.message.edit_text(text=f"Test-1\n{list(worddict.keys())[0]}\nJavobni tanlang", reply_markup=variantlar(
        correct=worddict[list(worddict.keys())[0]],
        values=list(worddict.values()),
        kategory=kategory.get('id')
    )
    )
    # await call.message.delete()


@dp.callback_query_handler(lambda c: str(c.data).startswith('togri') or str(c.data).startswith('notogri'), state="soz_yodlash")
async def checktest(call: CallbackQuery, state: FSMContext):
    await call.answer()
    count = int(call.message.text.split("\n")[0].split("-")[1])
    data, kategory_id = call.data.split(":")
    kategory = await db.select_category(int(kategory_id))

    statedata = await state.get_data()
    if data == "togri":
        await state.update_data({'togri': int(statedata.get('togri', 0))+1})
    else:
        await state.update_data({'notogri': int(statedata.get('notogri', 0))+1})
    statedata = await state.get_data()
    if len(kategory.get('word_id_list')) == count:
        togrilar = statedata.get("togri")
        notogrilar = statedata.get("notogri")
        if not togrilar:
            togrilar = 0
        if not notogrilar:
            notogrilar = 0
        text = ""
        if togrilar == count:
            await call.message.edit_text(f"Siz Hamma testlarga to'g'ri javob berdingiz")
        elif notogrilar == count:
            await call.message.edit_text(f"Siz hamma testlarga noto'g'ri javob berdingiz")
        else:
            await call.message.edit_text(f"Siz {togrilar}ta to'g'ri\n{notogrilar}ta noto'g'ri javob berdingiz")
        await call.message.answer("Bo'limlardan qiziqarlisini tanlang", reply_markup=bolimlar())
        await state.finish()
        return

    words = []
    for i in kategory.get('word_id_list'):
        words.append(await db.select_word(id=int(i)))
    worddict = {}
    for i in words:
        worddict[i.get('eng')] = i.get('uz')
    await call.message.edit_text(text=f"Test-{str(count+1)}\n{str(list(worddict.keys())[count])}\nJavobni tanlang", reply_markup=variantlar(
        correct=worddict[list(worddict.keys())[count]],
        values=list(worddict.values()),
        kategory=kategory.get('id')
    )
    )
