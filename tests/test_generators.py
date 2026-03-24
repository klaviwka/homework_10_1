# src/tests/test_generators.py

import pytest
from src.generators import filter_by_currency, card_number_generator, transaction_descriptions


# Фикстуры с подготовленными списками транзакций
@pytest.fixture
def empty_transactions():
    """Возвращает пустой список транзакций."""
    return []


@pytest.fixture
def no_usd_transactions():
    """Возвращает список транзакций без USD."""
    return [
        {
            "id": 123456789,
            "state": "EXECUTED",
            "date": "2023-06-10T12:00:00Z",
            "operationAmount": {
                "amount": "1000.00",
                "currency": {"name": "EUR", "code": "EUR"}
            },
            "description": "Покупка товаров",
            "from": "Счет 1234567890",
            "to": "Счет 9876543210"
        },
        {
            "id": 987654321,
            "state": "EXECUTED",
            "date": "2023-06-11T13:00:00Z",
            "operationAmount": {
                "amount": "2000.00",
                "currency": {"name": "RUB", "code": "RUB"}
            },
            "description": "Оплата услуг",
            "from": "Счет 9876543210",
            "to": "Счет 1234567890"
        }
    ]


@pytest.fixture
def mixed_transactions():
    """Возвращает смешанный список транзакций с разными валютами."""
    return [
        {
            "id": 123456789,
            "state": "EXECUTED",
            "date": "2023-06-10T12:00:00Z",
            "operationAmount": {
                "amount": "1000.00",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Покупка товаров",
            "from": "Счет 1234567890",
            "to": "Счет 9876543210"
        },
        {
            "id": 987654321,
            "state": "EXECUTED",
            "date": "2023-06-11T13:00:00Z",
            "operationAmount": {
                "amount": "2000.00",
                "currency": {"name": "RUB", "code": "RUB"}
            },
            "description": "Оплата услуг",
            "from": "Счет 9876543210",
            "to": "Счет 1234567890"
        },
        {
            "id": 567890123,
            "state": "EXECUTED",
            "date": "2023-06-12T14:00:00Z",
            "operationAmount": {
                "amount": "3000.00",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Перевод средств",
            "from": "Счет 5678901230",
            "to": "Счет 0123456789"
        }
    ]


@pytest.fixture
def one_transaction():
    """Возвращает одну транзакцию."""
    return [
        {
            "id": 123456789,
            "state": "EXECUTED",
            "date": "2023-06-10T12:00:00Z",
            "operationAmount": {
                "amount": "1000.00",
                "currency": {"name": "USD", "code": "USD"}
            },
            "description": "Покупка товаров",
            "from": "Счет 1234567890",
            "to": "Счет 9876543210"
        }
    ]


# Тестируемые сценарии
@pytest.mark.parametrize(
    "transactions_fixture,currency,expected",
    [
        ("empty_transactions", "USD", []),
        ("no_usd_transactions", "USD", []),
        ("mixed_transactions", "USD", [
            {
                "id": 123456789,
                "state": "EXECUTED",
                "date": "2023-06-10T12:00:00Z",
                "operationAmount": {
                    "amount": "1000.00",
                    "currency": {"name": "USD", "code": "USD"}
                },
                "description": "Покупка товаров",
                "from": "Счет 1234567890",
                "to": "Счет 9876543210"
            },
            {
                "id": 567890123,
                "state": "EXECUTED",
                "date": "2023-06-12T14:00:00Z",
                "operationAmount": {
                    "amount": "3000.00",
                    "currency": {"name": "USD", "code": "USD"}
                },
                "description": "Перевод средств",
                "from": "Счет 5678901230",
                "to": "Счет 0123456789"
            }
        ]),
    ],
)
def test_filter_by_currency(request, transactions_fixture, currency, expected):
    """Тестирование функции filter_by_currency.
    """
    transactions = request.getfixturevalue(transactions_fixture)
    result = list(filter_by_currency(transactions, currency))
    assert result == expected


# Параметризованные тесты
@pytest.mark.parametrize(
    "start, stop, expected_cards",
    [
        (1, 5, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003",
                "0000 0000 0000 0004", "0000 0000 0000 0005"]),
        (1000, 1002, ["0000 0000 0000 1000", "0000 0000 0000 1001", "0000 0000 0000 1002"])
    ]
)
def test_card_numbers(start, stop, expected_cards):
    """
    Тестируем генерацию номеров карт.
    """
    generated_cards = list(card_number_generator(start, stop))
    assert generated_cards == expected_cards, f"Ошибка в генерации карт {generated_cards} != {expected_cards}"


# Тест на проверку остановки генератора
def test_stop_iteration():
    """
    Проверяем, что генератор корректно завершает работу.
    """
    generator = card_number_generator(1, 5)  # Убедитесь, что передаете необходимые аргументы
    # Получаем все доступные карты
    cards = list(generator)
    # Проверяем длину полученных карт
    assert len(cards) == 5, "Количество карт не соответствует заданному диапазону"


# Тест на корректность форматирования карты
def test_card_format():
    """
    Проверяем, что номера карт формируются корректно (разделяются на группы по 4 символа).
    """
    sample_card = next(card_number_generator(1, 1))  # Передаем параметры для генерации
    parts = sample_card.split()
    assert len(parts) == 4, "Неверное количество групп в номере карты"
    assert all(len(part) == 4 for part in parts), "Каждая группа должна содержать ровно 4 символа"


# Тест на некорректные входные данные
@pytest.mark.parametrize(
    "start_value",
    ["abc", -1, None]  # Добавляем другие некорректные значения для проверки
)
def test_invalid_start_value(start_value):
    """
    Проверяем, что функция корректно обрабатывает некорректные входные данные.
    """
    # Проверяем, что при некорректных данных генерируется ошибка TypeError или ValueError
    with pytest.raises((TypeError, ValueError)):
        next(card_number_generator(start_value, 1))  # Пробуем получить первую карту


# Параметризованные тесты
@pytest.mark.parametrize(
    "expected, transactions_fixture",
    [
        ([], "empty_transactions"),                     # Пустой список транзакций
        (["Покупка товаров"], "one_transaction"),       # Одна транзакция
        (["Покупка товаров", "Оплата услуг", "Перевод средств"], "mixed_transactions")  # Несколько транзакций
    ]
)
def test_transaction_descriptions(request, expected, transactions_fixture):
    """
    Тестируем функцию transaction_descriptions.
    """
    transactions = request.getfixturevalue(transactions_fixture)
    result = list(transaction_descriptions(transactions))
    assert result == expected, f"Полученные описания: {result}. Ожидается: {expected}"
