from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup


user_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton('Пн'),
    KeyboardButton('Вт'),
    KeyboardButton('Ср'),
    KeyboardButton('Чт'),
    KeyboardButton('Пт'),
    KeyboardButton('Сб'),
    KeyboardButton('Вс'),
    KeyboardButton('Сегодня'),
    KeyboardButton('Завтра'))
