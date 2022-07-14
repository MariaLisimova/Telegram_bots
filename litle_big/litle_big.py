from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging
import os
import aiofiles


bot = Bot()
dp = Dispatcher(bot)

number = 100
count_of_attempts = 1


@dp.message_handler(commands='start')
async def start_message(message: types.Message):
    if count_of_attemps == 1:
        await bot.send_message(message.from_user.id, f'Привет, {message.from_user.full_name}, я загадал число '
                                                     f'попробуй его угадать')
    else:
        await bot.send_message(message.from_user.id, 'Введите число')


@dp.message_handler()
async def info(message: types.Message):
    global number, count_of_attempts

    try:
        if int(message.text) == number:
            await message.answer(f'Поздравляю, вы угадали!\nКоличество попыток: {count_of_attempts}')
            count_of_attempts = 1
        elif int(message.text) < number:
            await message.answer('Ваше число меньше загаданного\nПопробуй еще раз!')
            count_of_attempts += 1
        else:
            await message.answer('Ваше число больше загаданного\nПопробуй еще раз!')
            count_of_attempts += 1
    except:
        await bot.send_message(message.from_user.id, f'Привет, {message.from_user.full_name}, я загадал число '
                                                     f'попробуй его угадать')


if __name__ == '__main__':
    print('Бот запущен')
    executor.start_polling(dp)