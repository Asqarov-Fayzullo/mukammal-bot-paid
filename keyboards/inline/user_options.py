from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

def tillar():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Rus-tili🇷🇺",callback_data='rus'),
                InlineKeyboardButton(text="Ingliz tili  🇺🇸",callback_data="ingliz"),
            ],
        ],
        row_width=2
    )

def bolimlar():
    return InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Kategoriyalar",callback_data="categories"),
        ],
        [
            InlineKeyboardButton(text="So'z yodlash",callback_data="soz_yodlash"),
        ],
        [
            InlineKeyboardButton(text="Yangi so'z qo'shish",callback_data="yangi_soz"),
        ]
    ],
    row_width=2
)


def tillar_for_new_word():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Rus-tili🇷🇺",callback_data='rusadd'),
                InlineKeyboardButton(text="Ingliz tili  🇺🇸",callback_data="inglizadd"),
            ],
        ],
        row_width=2
    )

def tasdiqlash(adder=""):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("✅",callback_data=f"togri:{adder}"),
                InlineKeyboardButton("❌",callback_data=f"notogri:{adder}")
            ],
        ],
        row_with=1
    )

def user_word_categories(categorylist=[],key=""):
    markup = InlineKeyboardMarkup(
        row_width=1
    )
    for kategory in categorylist:
        markup.add(InlineKeyboardButton(text=kategory.get('title'),callback_data='iskategory-'+key+str(kategory.get('id'))))
    
    markup.add(InlineKeyboardButton(text="orqaga",callback_data="orqaga"+key))
    if not key:
        markup.add(InlineKeyboardButton(text="+ Kategoriya qo'shish",callback_data="add_kategory"))
    return markup

def manage_kategory(kategory_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="+ So'z qo'shish",callback_data="add_word_to_kategory:{}".format(kategory_id)),
            ],
            [
                InlineKeyboardButton(text="Kategorydagi so'zlar",callback_data=f"kategory_words:{kategory_id}")
            ],
            # [
            #     InlineKeyboardButton(text="So'z yodlash",callback_data="start_learning_in_kategory:{}".format(kategory_id)),
            # ],
            [
                InlineKeyboardButton(text="Kategoryani o'chirish",callback_data=f"delete_kategory:{kategory_id}")
            ],
            [
                InlineKeyboardButton(text="orqaga",callback_data="kategories_statega_qaytish")
            ]
        ],
        row_width=1
    )
    return markup

def get_new_word_id():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("IDni olish",callback_data="get_new_word_id")
            ]
        ]
    )
    