"""
Модуль для создания клавиатур бота.
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Основное меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("Случайная цитата"))
main_menu.add(KeyboardButton("Поиск по слову"))
main_menu.add(KeyboardButton("Поиск по автору"))