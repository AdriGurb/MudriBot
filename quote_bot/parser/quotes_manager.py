"""
Модуль для управления цитатами.
"""

import random
from parser.exceptions import ParsingError
from parser.quote_scraper import QuoteScraper

class QuoteManager:
    """
    Класс для управления списком цитат.
    """

    def __init__(self):
        """Инициализация менеджера цитат."""
        self.scraper = QuoteScraper()
        self.quotes = self.scraper.get_quotes()

    def get_random_quote(self) -> str:
        """Получение случайной цитаты."""
        if not self.quotes:
            raise ParsingError("Список цитат пуст.")
        return random.choice(self.quotes)

    def search_by_word(self, word: str) -> str:
        """
        Поиск цитаты по слову.

        :param word: Слово для поиска
        :return: Найденная цитата
        """
        if not isinstance(word, str):
            raise ValueError("Аргумент 'word' должен быть строкой.")
        matches = [q for q in self.quotes if word.lower() in q.lower()]
        return random.choice(matches) if matches else None

    def search_by_author(self, author: str) -> str:
        """
        Поиск цитат по автору.

        :param author: Имя автора
        :return: Найденные цитаты
        """
        if not isinstance(author, str):
            raise ValueError("Аргумент 'author' должен быть строкой.")
        matches = [q for q in self.quotes if author.lower() in q.lower()]
        return "\n———\n".join(matches) if matches else None