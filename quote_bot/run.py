"""
Модуль запуска Telegram-бота с мотивирующими цитатами.
"""

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from keyboards import main_menu
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from parser.quotes_manager import QuoteManager
from parser.exceptions import ParsingError

# Состояния
class SearchStates(StatesGroup):
    """Состояния для поиска цитат."""
    word_search = State()
    author_search = State()

# Инициализация бота

bot = Bot('7813176938:AAGky9mYbYMOSYTtgISgEtz5Xm_O38m5dVc')
dp = Dispatcher(bot, storage=MemoryStorage())

# Инициализация менеджера цитат
quote_manager = QuoteManager()

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    """Обработка команды /start."""
    await message.answer("Привет! Я бот с мотивирующими цитатами. Выберите действие:", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "Случайная цитата")
async def random_quote(message: types.Message):
    """Обработка кнопки "Случайная цитата"."""
    try:
        random_quote = quote_manager.get_random_quote()
        await message.answer(random_quote)
    except ParsingError as e:
        await message.answer(f"Ошибка: {str(e)}")

@dp.message_handler(lambda message: message.text == "Поиск по слову")
async def search_quote_by_word(message: types.Message, state: FSMContext):
    """Обработка кнопки "Поиск по слову"."""
    await SearchStates.word_search.set()
    await message.answer("Введите слово для поиска цитаты:")

@dp.message_handler(state=SearchStates.word_search)
async def handle_word_input(message: types.Message, state: FSMContext):
    """Обработка ввода слова для поиска цитаты."""
    word = message.text
    try:
        filtered_quote = quote_manager.search_by_word(word)
        if filtered_quote:
            await message.answer(filtered_quote)
        else:
            await message.answer("Цитаты с таким словом не найдены.")
    finally:
        await state.finish()

@dp.message_handler(lambda message: message.text == "Поиск по автору")
async def search_quote_by_author(message: types.Message, state: FSMContext):
    """Обработка кнопки "Поиск по автору"."""
    await SearchStates.author_search.set()
    await message.answer("Введите имя автора для поиска цитат:")

@dp.message_handler(state=SearchStates.author_search)
async def handle_author_input(message: types.Message, state: FSMContext):
    """Обработка ввода имени автора для поиска цитат."""
    author = message.text
    try:
        filtered_quotes = quote_manager.search_by_author(author)
        if filtered_quotes:
            await message.answer(filtered_quotes)
        else:
            await message.answer("Цитаты с таким автором не найдены.")
    finally:
        await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)