import re
from collections import Counter
from datetime import datetime


def filter_by_state(transactions, state='EXECUTED'):
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param transactions: Список словарей с транзакциями.
    :param state: Значение для фильтрации по ключу 'state'. По умолчанию 'EXECUTED'.
    :return: Новый список словарей, содержащий только те, у которых ключ 'state' соответствует указанному значению.
    """
    filtered_transactions = [transaction for transaction in transactions if transaction.get('state') == state]
    return filtered_transactions


def sort_by_date(transactions, descending=True):
    """
    Сортирует список словарей по значению ключа 'date'.

    :param transactions: Список словарей с транзакциями.
    :param descending: Параметр, задающий порядок сортировки. По умолчанию True (по убыванию).
    :return: Новый список словарей, отсортированный по дате.
    """
    sorted_transactions = sorted(transactions, key=lambda x: datetime.fromisoformat(x['date']), reverse=descending)
    return sorted_transactions


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """
    Возвращает список словарей с банковской операцией, содержащей указанную строку в описании.

    :param data: Список словарей с данными о банковских операциях.
    :param search: Строка поиска.
    :return: Список словарей, содержащих искомую строку в описании.
    """
    results = []
    for record in data:
        if 'description' in record and re.search(search, record['description'], re.IGNORECASE):
            results.append(record)
    return results


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """
    Возвращает словарь, где ключи — это названия категорий,
    а значения — количество операций в каждой категории.

    :param data: Список словарей с данными о банковских операциях.
    :param categories: Список категорий для группировки.
    :return: Словарь с количеством операций по каждой категории.
    """
    counter = Counter()
    for record in data:
        if 'description' in record:
            for cat in categories:
                if cat.lower() in record['description'].lower():
                    counter[cat] += 1
    return dict(counter)


# Пример входных данных
transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364', 'description': 'Зарплата'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572', 'description': 'Коммунальные услуги'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689', 'description': 'Зарплата'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441', 'description': 'Транспорт'}
]

# Пример использования новой функции
categories = ['зарплата', 'коммунальные услуги']
result = process_bank_operations(transactions, categories)
print(result)
