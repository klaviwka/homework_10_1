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
    amount_str = transaction["operationAmount"]["amount"]
    currency = transaction["operationAmount"]["currency"]["code"]

    # Преобразуем строку с суммой в число с плавающей запятой
    amount = float(amount_str)

    if currency == "RUB":
        return amount
    elif currency in ["USD", "EUR"]:
        api_key = os.getenv("API_KEY")  # Здесь используем вашу переменную API_KEY
        if not api_key:
            raise ValueError("Необходимо задать API_KEY в переменных окружения!")

        response = requests.get(
            f"http://api.exchangeratesapi.io/v1/latest?access_key={api_key}&base={currency}"
        )

        if response.status_code != 200:
            raise RuntimeError(f"Ошибка запроса к API: статус-код {response.status_code}, сообщение: {response.text}")

        rates = response.json().get("rates", {})
        ruble_rate = rates.get("RUB")
        if ruble_rate is None:
            raise ValueError(f"Нет данных о курсе {currency} к RUB")

        return round(float(amount * ruble_rate), 2)
    else:
        raise ValueError(f"Валюта '{currency}' не поддерживается.")
