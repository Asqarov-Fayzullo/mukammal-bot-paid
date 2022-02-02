from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from data.config import ADMINS
class CallbackAdminFilter(BoundFilter):
    async def check(self,call:types.CallbackQuery):
        if str(call.message.chat.id) in ADMINS:
            return True