import requests
from bs4 import BeautifulSoup
from parser.exceptions import ParsingError

class QuoteScraper:
    """
    Класс для парсинга цитат с сайта.
    """

    URL = "https://www.forbes.ru/forbeslife/dosug/262327-na-vse-vremena-100-vdokhnovlyayushchikh-tsitat"

    def get_quotes(self) -> list[str]:
        """
        Получение списка цитат с сайта.

        :return: Список цитат
        """
        response = requests.get(self.URL)
        if response.status_code != 200:
            raise ParsingError(f"Ошибка при запросе: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")
        quotes_html = soup.find_all("p", itemprop="articleBody")

        quotes = []
        for i in range(0, len(quotes_html), 2):
            # Извлечение текста цитаты и удаление лишних символов в начале строки
            text = quotes_html[i].get_text(strip=True)
            text = self._clean_quote_text(text)

            # Извлечение автора цитаты
            author = quotes_html[i + 1].get_text(strip=True) if i + 1 < len(quotes_html) else "Неизвестный автор"
            
            quotes.append(f"{text}\n — {author}")

        return quotes

    def _clean_quote_text(self, text: str) -> str:
        """
        Очищает текст цитаты от всех символов и цифр в начале строки до первой буквы.
        
        :param text: Исходный текст цитаты
        :return: Очищенный текст цитаты, начинающийся с буквы
        """
        # Ищем первый символ, который является буквой и обрезаем строку до этого символа
        i = 0
        while i < len(text) and not text[i].isalpha():
            i += 1
        return text[i:]  # Возвращаем строку, начиная с первого буквенного символа