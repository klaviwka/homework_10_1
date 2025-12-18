from datetime import datetime


def filter_by_state(transactions, state='EXECUTED'):
    """
    Фильтрует список словарей по значению ключа 'state'.

    :param transactions: Список словарей с транзакциями.
    :param state: Значение для фильтрации по ключу 'state'. По умолчанию 'EXECUTED'.
    :return: Новый список словарей, содержащий только те, у которых ключ 'state' соответствует указанному значению.
    """
    print(f"Фильтрация транзакций по состоянию: {state}...")
    filtered_transactions = [transaction for transaction in transactions if transaction.get('state') == state]
    print(f"Найдено {len(filtered_transactions)} транзакций с состоянием '{state}'.")
    return filtered_transactions


def sort_by_date(transactions, descending=True):
    """
    Сортирует список словарей по значению ключа 'date'.

    :param transactions: Список словарей с транзакциями.
    :param descending: Параметр, задающий порядок сортировки. По умолчанию True (по убыванию).
    :return: Новый список словарей, отсортированный по дате.
    """
    order = "по убыванию" if descending else "по возрастанию"

    print(f"Сортировка транзакций {order}...")
    sorted_transactions = sorted(transactions, key=lambda x: datetime.fromisoformat(x['date']), reverse=descending)
    print(f"Транзакции отсортированы {order}.")
    return sorted_transactions


# Пример входных данных
transactions = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
    {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
]

# Пример использования функций
executed_transactions = filter_by_state(transactions)
print("\nИсполненные транзакции:")
print(executed_transactions)

canceled_transactions = filter_by_state(transactions, state='CANCELED')
print("\nОтмененные транзакции:")
print(canceled_transactions)

sorted_transactions_desc = sort_by_date(transactions)
print("\nСортировка по дате (по убыванию):")
print(sorted_transactions_desc)

sorted_transactions_asc = sort_by_date(transactions, descending=False)
print("\nСортировка по дате (по возрастанию):")
print(sorted_transactions_asc)
