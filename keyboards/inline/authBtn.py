from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def authBtn():
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(InlineKeyboardButton(text="Sign up", callback_data='sign_up'))
    btn.add(InlineKeyboardButton(text="Sign in", callback_data='sign_in'))
    return btn