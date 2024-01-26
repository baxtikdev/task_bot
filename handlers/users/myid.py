from aiogram import types

from loader import dp


@dp.message_handler(state='*', commands=['myid'])
async def myID(message: types.Message):
    await message.reply(text=f"`{message.from_user.id}`")
