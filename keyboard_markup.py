from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardButton

builder = InlineKeyboardBuilder()
builder.row(
    InlineKeyboardButton(text="GitHub", url="https://github.com/znakar"),
    InlineKeyboardButton(text="YouTube", url="https://www.youtube.com/"),
    InlineKeyboardButton(text="Images", callback_data="images"),
    InlineKeyboardButton(text="Back", callback_data = "whatever")
)

markup = builder.as_markup()
