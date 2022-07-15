from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup
from aiogram.utils import executor
import logging
import os
import datetime


bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_message(message: types.Message):
    await bot.send_message(message.from_user.id, f'Привет {message.from_user.first_name}, Я бот который отправит '
                                                 f'тебе твое же сообщение', reply_markup=user_kb)
    await bot.send_message(message.from_user.id, 'Можешь узнать дату', reply_markup=user_inline_kb)


@dp.message_handler(text='Пожелание доброго утра')
async def good_morning(message: types.Message):
    await bot.send_message(message.from_user.id, 'Доброе утро!')


@dp.message_handler(text='Пожелание доброй ночи')
async def good_night(message: types.Message):
    await bot.send_message(message.from_user.id, 'Доброй ночи!🌙')


@dp.callback_query_handler(text='button_date')
async def date_message(callback_quary):
    await bot.answer_callback_query(callback_quary.id, 'Кнопка сработала', show_alert=True)

    now_date = datetime.datetime.now()

    await bot.send_message(callback_quary.from_user.id, f"{now_date.strftime('%d.%m.%Y %H:%M:%S')}")


@dp.message_handler()
async def reply_message(message: types.Message):
    await message.reply(message.text)

"""*******************************   BUTTONS   *******************************"""
button_good_morning = KeyboardButton('Пожелание доброго утра')
button_good_night = KeyboardButton('Пожелание доброй ночи')

# user_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(button_good_morning).add(button_good_night)
user_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_good_morning)\
    .add(button_good_night)


button_date = InlineKeyboardButton(text='Время и дата', callback_data='button_date')
user_inline_kb = InlineKeyboardMarkup().add(button_date)


if __name__ == '__main__':
    print('bot polling started')
    executor.start_polling(dp)