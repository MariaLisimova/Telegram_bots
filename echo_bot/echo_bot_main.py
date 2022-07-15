from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import logging
import os

logging.basicConfig(level=logging.DEBUG, filename='mylog.log',
                    format='%(asctime)s | %(levelname)s | %(funcName)s: %(lineno)d | %(message)s',
                    datefmt='%H:%M:%S')

bot = Bot(os.environ.get('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_message(message: types.Message):
    await bot.send_message(message.from_user.id, f'Привет,{message.from_user.full_name},я бот,'
                                                 f'который отправит в ответ любое твое сообщение')


@dp.message_handler()
async def start_message(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)


if __name__ == '__main__':
    print('bot polling started')
    executor.start_polling(dp)
    