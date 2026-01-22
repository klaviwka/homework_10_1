import pytest
from src.processing import filter_by_state, sort_by_date

# Фиктура для тестовых данных транзакций
@pytest.fixture
def test_transactions():
    """Возвращает список тестовых транзакций."""
    return [
        {'id': 1, 'amount': 100, 'state': 'EXECUTED'},
        {'id': 2, 'amount': 200, 'state': 'CANCELLED'},
        {'id': 3, 'amount': 300, 'state': 'EXECUTED'},
        {'id': 4, 'amount': 400, 'state': 'PENDING'},
        {'id': 5, 'amount': 500, 'state': 'EXECUTED'},
    ]

# Тест фильтрации по состоянию EXECUTED
def test_filter_by_state_executed(test_transactions):
    """Тестирует фильтрацию транзакций по состоянию EXECUTED."""
    result = filter_by_state(test_transactions, state='EXECUTED')
    expected = [
        {'id': 1, 'amount': 100, 'state': 'EXECUTED'},
        {'id': 3, 'amount': 300, 'state': 'EXECUTED'},
        {'id': 5, 'amount': 500, 'state': 'EXECUTED'},
    ]
    assert result == expected

# Тест фильтрации по состоянию CANCELLED
def test_filter_by_state_cancelled(test_transactions):
    """Тестирует фильтрацию транзакций по состоянию CANCELLED."""
    result = filter_by_state(test_transactions, state='CANCELLED')
    expected = [{'id': 2, 'amount': 200, 'state': 'CANCELLED'}]
    assert result == expected

# Тест фильтрации по состоянию PENDING
def test_filter_by_state_pending(test_transactions):
    """Тестирует фильтрацию транзакций по состоянию PENDING."""
    result = filter_by_state(test_transactions, state='PENDING')
    expected = [{'id': 4, 'amount': 400, 'state': 'PENDING'}]
    assert result == expected

# Тест фильтрации по несуществующему состоянию
def test_filter_by_state_non_existent(test_transactions):
    """Тестирует фильтрацию транзакций по несуществующему состоянию."""
    result = filter_by_state(test_transactions, state='NON_EXISTENT')
    expected = []
    assert result == expected

# Тест фильтрации по умолчанию (состояние EXECUTED)
def test_filter_by_state_default(test_transactions):
    """Тестирует фильтрацию транзакций по умолчанию (состояние EXECUTED)."""
    result = filter_by_state(test_transactions)  # По умолчанию состояние EXECUTED
    expected = [
        {'id': 1, 'amount': 100, 'state': 'EXECUTED'},
        {'id': 3, 'amount': 300, 'state': 'EXECUTED'},
        {'id': 5, 'amount': 500, 'state': 'EXECUTED'},
    ]
    assert result == expected

# Фиктура для тестовых данных транзакций с датами
@pytest.fixture
def test_date_transactions():
    """Возвращает список тестовых транзакций с датами."""
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]

# Параметризованный тест для сортировки по дате
@pytest.mark.parametrize("descending, expected_order", [
    (True, [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    ]),
    (False, [
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    ]),
])
def test_sort_by_date(test_date_transactions, descending, expected_order):
    """Тестирует сортировку транзакций по дате."""
    result = sort_by_date(test_date_transactions, descending=descending)
    assert result == expected_order
