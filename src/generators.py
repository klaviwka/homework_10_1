def transaction_descriptions(transactions):
    """
    Генератор, который последовательно выдаёт описания транзакций.

    :param transactions: Список транзакций.
    :yield: Последовательные описания транзакций.
    """
    for transaction in transactions:
        yield transaction['description']


def card_number_generator(start=1, stop=9999999999999999):
    """
    Генерирует номера банковских карт от start до stop включительно.

    Формат номера карты: XXXX XXXX XXXX XXXX
    Параметры:
        start (int): Начальное значение диапазона (включительно)
        stop (int): Конечное значение диапазона (включительно)

    Возвращает:
        str: Следующий номер карты в формате XXXX XXXX XXXX XXXX
    """
    # Проверяем корректность входных данных
    if not isinstance(start, int) or not isinstance(stop, int):
        raise TypeError("Начальное и конечное значения должны быть целыми числами!")
    if start <= 0 or stop <= 0:
        raise ValueError("Значения должны быть положительными!")
    if start > stop:
        raise ValueError("Начало диапазона должно быть меньше или равно концу диапазона!")

    for number in range(start, stop + 1):
        formatted_card = f"{number:016d}"
        formatted_card = " ".join([formatted_card[i:i+4] for i in range(0, len(formatted_card), 4)])
        yield formatted_card


def filter_by_currency(transactions, currency):
    """
    Фильтрация транзакций по заданной валюте.

    :param transactions: Список транзакций.
    :param currency: Код валюты (например, "USD").
    :return: Итератор по транзакциям с заданной валютой.
    """
    return (
        transaction for transaction in transactions if transaction["operationAmount"]["currency"]["code"] == currency
    )
