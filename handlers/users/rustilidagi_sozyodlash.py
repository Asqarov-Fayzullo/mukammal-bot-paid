# from aiogram import types
# from aiogram.dispatcher import FSMContext
# from aiogram.types import CallbackQuery

# from loader import dp,db,bot
# from keyboards.inline.test_variantlari import variantlar_yaratish
# from keyboards.inline.user_options import qayta_test
# from states.soz_yodlash import TestState

# from utils.misc.shuffle import create_value_list

# #Test qilish qismi
# @dp.callback_query_handler(state=TestState)
# async def tekshir(call:CallbackQuery,state:FSMContext):
#     userid = call.message.chat.id

#     data = call.data
#     words = await db.get_primary_words(telegram_id=userid)
#     message_text = call.message.text
#     message_word = message_text.split('\n')[1]
#     user = await db.select_user(telegram_id=userid)
#     user_poll_number = int(user.get('poll_index'))

#     if words[message_word] == data.replace('-javob', ''):
#         await db.update_correct_id(telegram_id=userid,correct_id=1)
#         await call.answer("To'g'ri!")
#     else:
#         await db.update_user_selects(telegram_id=userid,select_id=1)
#         await call.answer("Xato!")
#     await call.message.delete()
#     await bot.delete_message(userid, call.message.message_id - 1)
#     if user_poll_number==14:
#         userid = call.message.chat.id
#         user = await db.select_user(telegram_id=userid)
#         corrects = user.get('correct_test_id')
#         notcorrects = user.get("user_selects")
#         if corrects == None:
#             corrects = []
#         if notcorrects == None:
#             notcorrects = []
#         if len(corrects) == 15:
#             await call.message.answer(
#                 "Hamma testga to'g'ri jaob berib keyingi bosqichga o'tdingiz yangi sozlarni hoziroq yodlashni boshlashingiz mumkin",
#                 reply_markup=qayta_test)
#         elif len(corrects) == 0 and len(notcorrects) > 0:
#             await call.message.answer("Hamma testga noto'g'ri javob berdingiz qayta urinib ko'ring",
#                                       reply_markup=qayta_test)
#         else:
#             if len(corrects) == 0 and len(notcorrects) == 0:
#                 await call.message.answer(f"Boshlanmasdan yakunlab qo'ydizu qayta boshlaymizmi",
#                                           reply_markup=qayta_test)
#             elif len(corrects) > 0 and len(notcorrects) == 0:
#                 await call.message.answer(f"{len(corrects)}ta to'g'ri javob berdiz qayta urinib ko'rasizmi?",
#                                           reply_markup=qayta_test)

#             else:
#                 await call.message.answer(f"Siz {len(corrects)}ta to'g'ri va {len(notcorrects)}ta xato javob berdingiz",reply_markup=qayta_test)
#         await state.finish()
#         return
#         return
#     word = list(words.keys())[user_poll_number+1]
#     markup = variantlar_yaratish(create_value_list(words[word], list(words.values())))
#     word_on_db = await db.select_word(ru=word)
#     audio = word_on_db.get("mp3_file_id")
#     await call.message.answer_audio(audio=audio)
#     await call.message.answer(text=f"Test-{user_poll_number + 2}:\n{word}\n so'z tarjimasini tanlang👇", reply_markup=markup)
#     await db.update_user_poll_index(userid)
