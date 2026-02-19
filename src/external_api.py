# external_api.py

import os
import requests
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()


def convert_transaction_to_rubles(transaction):
    """
    Конвертирует сумму транзакции в рубли. Если сумма указана в USD или EUR,
    производится запрос к внешнему API для получения текущего курса и выполняется конвертация.

    :param transaction: Словарь с данными транзакции.
    :return: Сумма транзакции в рублях (тип float).
    """
    amount_str = transaction["operationAmount"]["amount"]  # Получаем сумму транзакции
    currency = transaction["operationAmount"]["currency"]["code"]  # Получаем валюту транзакции

    # Преобразуем строку с суммой в число с плавающей точкой
    amount = float(amount_str)

    if currency == "RUB":
        return amount  # Если валюта уже рубли, возвращаем сумму без конвертации

    elif currency in ["USD", "EUR"]:
        api_key = os.getenv("API_KEY")  # Берём API KEY из переменных окружения
        if not api_key:
            raise ValueError("Необходимо задать API_KEY в переменных окружения.")

        headers = {
            "apikey": api_key  # Устанавливаем заголовок с API ключом
        }

        # Формируем тело запроса для API exchangerates_data
        params = {
            "to": "RUB",      # Валюта, в которую конвертируем
            "from": currency,  # Исходная валюта
            "amount": amount   # Сумму, которую конвертируем
        }

        # Отправляем GET-запрос к API
        response = requests.get(
            "https://api.apilayer.com/exchangerates_data/convert",
            headers=headers,
            params=params
        )

        if response.status_code != 200:
            raise RuntimeError(f"Ошибка запроса к API: статус-код {response.status_code}, сообщение: {response.text}")

        # Получаем ответ и извлекаем значение по ключу "result"
        converted_amount = response.json().get("result")
        if converted_amount is None:
            raise ValueError("Не удалось получить значение по ключу 'result'")

        return round(converted_amount, 2)  # Округляем результат до двух знаков после запятой

    else:
        raise ValueError(f"Валюта '{currency}' не поддерживается.")
