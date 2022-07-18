from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

bot = Bot('5555683553:AAHsG8bi9GRkN3BzqcGqWG0prRQcDea407k')
dp = Dispatcher(bot, storage=MemoryStorage())
admin_id = 5424187874

users = {}


class FSMAdmin(StatesGroup):
    show_info = State()
    get_loging = State()
    get_password = State()
    accept = State()


@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Ввод отменен', reply_markup=user_start_kb)
    await state.finish()


@dp.message_handler(commands='start')
async def start_mess(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=user_start_kb)
        await FSMAdmin.show_info.set()
    else:
        await bot.send_message(message.from_user.id, 'Вы не имеете прав для работы с этим ботом')


@dp.message_handler(Text(equals='добавить аккаунт', ignore_case=True))
@dp.message_handler(state=FSMAdmin.show_info)
async def send_info(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Введите логин', reply_markup=cancel_button)
    await FSMAdmin.get_loging.set()


@dp.message_handler(state=FSMAdmin.get_loging)
async def get_loging(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['loging'] = message.text
    await FSMAdmin.get_password.set()
    await bot.send_message(message.from_user.id, 'Введите пароль', reply_markup=cancel_button)


@dp.message_handler(state=FSMAdmin.get_password)
async def get_password(message: types.Message, state: FSMContext):
    global loging, password
    async with state.proxy() as data:
        data['password'] = message.text

    loging = data.get('loging')
    password = data.get('password')

    await bot.send_message(message.from_user.id, f'Убедитесь в правильности введения данных\n\nЛогин: {loging}, '
                                                 f'Пароль: {password}', reply_markup=yes_no_kb)
    await FSMAdmin.accept.set()


@dp.message_handler(state=FSMAdmin.accept)
async def accept(message: types.Message, state: FSMContext):
    global loging, password, users
    if message.text == 'Да':
        users[loging] = password
        print(users)
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Ввод отменен', reply_markup=user_start_kb)
        await FSMAdmin.show_info.set()


"""*****************************  BUTTONS  ********************************"""
user_start_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Добавить аккаунт'))

cancel_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Отмена'))

choice_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Добавить'))\
    .add(cancel_button)

yes_no_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Да'))\
    .add(KeyboardButton('Нет'))

if __name__ == '__main__':
    print('bot polling started')
    executor.start_polling(dp, skip_updates=True)