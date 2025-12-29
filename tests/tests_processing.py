import pytest
from typing import List, Dict, Any

from src.processing import filter_by_state, sort_by_date


# Фикстура для тестовых данных
@pytest.fixture
def transactions() -> List[Dict[str, Any]]:
    """Возвращает список транзакций для тестирования."""
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]


# Тесты для функции filter_by_state
@pytest.mark.parametrize("input_state, expected_output", [
    ('EXECUTED', [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]),
    ('CANCELED', [
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]),
    ('UNKNOWN', [])
])
def test_filter_by_state(
    transactions: List[Dict[str, Any]],
    input_state: str,
    expected_output: List[Dict[str, Any]]
) -> None:
    """Тестирует функцию filter_by_state на различных состояниях транзакций."""
    assert filter_by_state(transactions, input_state) == expected_output


# Тесты для функции sort_by_date
@pytest.mark.parametrize("descending, expected_order", [
    (True, [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]),
    (False, [
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'}
    ])
])
def test_sort_by_date(
    transactions: List[Dict[str, Any]],
    descending: bool,
    expected_order: List[Dict[str, Any]]
) -> None:
    """Тестирует функцию sort_by_date на сортировку транзакций по дате."""
    assert sort_by_date(transactions, descending) == expected_order


# Запуск тестов
if __name__ == "__main__":
    pytest.main()
