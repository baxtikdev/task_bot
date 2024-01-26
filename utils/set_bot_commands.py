from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Botni ishga tushurish"),
            types.BotCommand("login", "Telegram orqali login qilish"),
            types.BotCommand("myid", "Mening telegram ID"),
            types.BotCommand("help", "Yordam"),
        ]
    )
