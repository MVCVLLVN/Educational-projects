from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
import sqlite3


db = sqlite3.connect('my_recipe.db')    # создаем БД
sql = db.cursor()    # создаем объект через который будем обращаться к БД

# создаем таблицу
sql.execute("""CREATE TABLE IF NOT EXISTS all_recipe (
                        name TEXT,
                        recipe TEXT,
                        type TEXT,
                        photo TEXT
                    )""")
db.commit()     # пишем если хоти внести изменения в БД


token = "YOUR TOKEN"

storage = MemoryStorage()   # временное хранилище
bot = Bot(token=token)   # сам бот
dp = Dispatcher(bot, storage=storage)


all_class = ReplyKeyboardMarkup(resize_keyboard=True)
cls_1 = KeyboardButton("Завтрак")
cls_2 = KeyboardButton("Обед")
cls_3 = KeyboardButton("Ужин")
cls_4 = KeyboardButton("Перекусы")
cls_5 = KeyboardButton("Назад")
all_class.add(cls_1, cls_2, cls_3, cls_4, cls_5)

box = ReplyKeyboardMarkup(resize_keyboard=True)
b1 = KeyboardButton(text='Добавить')
b2 = KeyboardButton(text='Посмотреть')
box.add(b1, b2)

data = list()


class SetData(StatesGroup):    # новое МАШИННОЕ СОСТОНИЕ
    name = State()
    recipe = State()  # конкретное состояние
    type_dish = State()  # конкретное состояние
    photo = State()  # конкретное состояние


class GetData(StatesGroup):    # новое МАШИННОЕ СОСТОНИЕ
    all_data = State()  # конкретное состояние
    current_data = State()  # конкретное состояние


@dp.message_handler(commands=["start"])     # Декоратор для определения команды. То есть фраза начинается с /
async def start(message: types.Message):

    await message.answer(text="Привет! Я хроню рецепты", reply_markup=box)


@dp.message_handler(content_types=["text"], state=GetData.all_data)     # Декоратор для определения команды
async def start(message: types.Message, state: FSMContext):
    global data
    if message.text == "Назад":
        await state.finish()
    sql.execute(f"SELECT * FROM all_recipe WHERE type = '{message.text}'")
    data = sql.fetchall()
    if data:
        cur_type = ReplyKeyboardMarkup(resize_keyboard=True)
        for elem in data:
            cur_type.add(KeyboardButton(text=f"{elem[0]}"))
        cur_type.add(KeyboardButton(text="Назад"))
        await message.answer(text="Выбери один из рецептов ужина", reply_markup=cur_type)
        await GetData.current_data.set()
    else:
        await message.answer(text="Такого типа блюд в БД еще нет...", reply_markup=box)
        await state.finish()


@dp.message_handler(content_types=["text"], state=GetData.current_data)     # Декоратор для определения команды
async def start(message: types.Message, state: FSMContext):
    if message.text == "Назад":
        await message.answer(text="Для какого типа блюда хотите посмотреть рецепт?", reply_markup=all_class)
        await GetData.all_data.set()
    else:
        for elem in data:
            if elem[0] == message.text:
                await bot.send_photo(chat_id=message.chat.id, caption=elem[1], photo=elem[3])
                break


@dp.message_handler(content_types=["text"], state=SetData.name)     # Декоратор для определения команды
async def start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["имя"] = message.text
    await message.answer(text="Теперь напишите состав блюда")
    await SetData.next()


@dp.message_handler(content_types=["text"], state=SetData.recipe)     # Декоратор для определения команды
async def start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["рецепт"] = message.text
    await message.answer(text="Отлично. К какому классу относится блюдо?", reply_markup=all_class)
    await SetData.next()


@dp.message_handler(content_types=["text"], state=SetData.type_dish)     # Декоратор для определения команды
async def start(message: types.Message, state: FSMContext):
    if message.text in ("Завтрак", "Обед", "Ужин", "Перекусы"):
        async with state.proxy() as data:
            data["тип"] = message.text
            await message.answer(text="И в заключении пришли фото!)")
            await SetData.next()
    else:
        await message.answer(text="НАЖМИТЕ КНОПКУ ДЛЯ ВЫБОРА ТИПА БЛЮДА!!!")


@dp.message_handler(content_types=["photo"], state=SetData.photo)     # Декоратор для определения команды
async def start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["фото"] = message.photo[0].file_id

    sql.execute("INSERT INTO all_recipe VALUES (?, ?, ?, ?)", (
        f'{data["имя"]}',
        f'{data["рецепт"]}',
        f'{data["тип"]}',
        f'{data["фото"]}'))
    db.commit()
    await message.answer(text=f'Данные добавлены!)', reply_markup=box)
    await state.finish()    # Завершаем МАШИНУ СОСТОЯНИЙ и выходим в основное


@dp.message_handler(content_types=["text"])     # Декоратор для определения команды. То есть фраза начинается с /
async def info(message: types.Message):
    if message.text == "Добавить":
        await message.answer(text="Напишите название блюда")
        await SetData.name.set()  # запускаем 1 состояние для сбора информации
    elif message.text == "Посмотреть":
        await message.answer(text="Для какого типа блюда хотите посмотреть рецепт?", reply_markup=all_class)
        await GetData.all_data.set()

executor.start_polling(dp, skip_updates=True)

