from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from save_loging_passworld_bot.db_bot import *
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
    get_info = State()
    delete_accounts = State()
    delete_login = State()


@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, 'Ввод отменен', reply_markup=user_start_kb)
    await state.finish()


@dp.message_handler(Text(equals=['добавить аккаунт', 'получить информацию', 'удалить все аккаунты',
                                 'удалить один аккаунт'], ignore_case=True))
async def start_choice(message: types .Message, state: FSMContext):
    if message.text == 'Добавить аккаунт':
        await bot.send_message(message.from_user.id, 'Введите логин', reply_markup=cancel_button)
        await FSMAdmin.get_loging.set()
    elif message.text == 'Удалить все аккаунты':
        await delete_all_accounts(message)
        await state.finish()
    elif message.text == 'Удалить один аккаунт':
        await bot.send_message(message.from_user.id, 'Введите логин аккаунта, который хотите удалить',
                               reply_markup=cancel_button)
        await FSMAdmin.delete_login.set()
    else:
        await sql_read_info(message=message)
        await state.finish()


@dp.message_handler(state=FSMAdmin.delete_login)
async def delete_account(message: types.Message, state: FSMContext):
    await delete_account_db(message=message, login=message.text)
    await state.finish()


@dp.message_handler(commands='start')
async def start_mess(message: types.Message, state: FSMContext):
    if message.from_user.id == admin_id:
        await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=user_start_kb)
        await FSMAdmin.show_info.set()
    else:
        await bot.send_message(message.from_user.id, 'Вы не имеете прав для работы с этим ботом')


@dp.message_handler(state=FSMAdmin.show_info)
async def send_info(message: types.Message, state: FSMContext):
    if message.text == 'Получить информацию':
        await sql_read_info(message)
        await state.finish()
    elif message.text == 'Удалить все аккаунты':
        await delete_all_accounts(message)
        await state.finish()
    elif message.text == 'Удалить один аккаунт':
        await bot.send_message(message.from_user.id, 'Введите логин аккаунта, который хотите удалить',
                               reply_markup=cancel_button)
        await FSMAdmin.delete_login.set()
    else:
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
    global login, password
    async with state.proxy() as data:
        data['password'] = message.text

    login = data.get('loging')
    password = data.get('password')

    await bot.send_message(message.from_user.id, f'Убедитесь в правильности введения данных\n\nЛогин: {login}, '
                                                 f'Пароль: {password}', reply_markup=yes_no_kb)
    await FSMAdmin.accept.set()


@dp.message_handler(state=FSMAdmin.accept)
async def accept(message: types.Message, state: FSMContext):
    global login, password, users
    if message.text == 'Да':
        try:
            await sql_add_account(login=login, password=password)
            await bot.send_message(message.from_user.id, 'Ваши данные успешно сохранены', reply_markup=user_start_kb)
            await state.finish()
        except Exception as ex:
            print(ex)
            await bot.send_message(message.from_user.id, 'Такой логин уже существует', reply_markup=user_start_kb)
            await FSMAdmin.show_info.set()
    else:
        await bot.send_message(message.from_user.id, 'Ввод отменен', reply_markup=user_start_kb)
        await state.finish()


"""*****************************  BUTTONS  ********************************"""
user_start_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('Добавить аккаунт'))\
    .add(KeyboardButton('Получить информацию')).add(KeyboardButton('Удалить все аккаунты'))\
    .add(KeyboardButton('Удалить один аккаунт'))

cancel_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Отмена'))

choice_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Добавить')) \
    .add(cancel_button)

yes_no_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(KeyboardButton('Да')) \
    .add(KeyboardButton('Нет'))

if __name__ == '__main__':
    print('bot polling started')
    sql_start()
    executor.start_polling(dp, skip_updates=True)
