# test_csv_excel_read.py

import unittest
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest  # добавляем подключение pytest

from src.csv_excel_read import read_csv_transactions, read_excel_transactions


def create_mock_df():
    """Создание фиктивного DataFrame с настоящими данными"""
    return pd.DataFrame({
        'id': [650703, 3598919, 593027],
        'state': ['EXECUTED', 'EXECUTED', 'CANCELED'],
        'date': ['2023-09-05T11:30:32Z', '2020-12-06T23:00:58Z', '2023-07-22T05:02:01Z'],
        'amount': [16210, 29740, 30368],
        'currency_name': ['Sol', 'Peso', 'Shilling'],
        'currency_code': ['PEN', 'COP', 'TZS'],
        'from': ['Счет 58803664561298323391', 'Discover 3172601889670065', 'Visa 1959232722494097'],
        'to': ['Счет 39745660563456619397', 'Discover 0720428384694643', 'Visa 6804119550473710'],
        'description': ['Перевод организации', 'Перевод с карты на карту', 'Перевод с карты на карту']
    })


def test_read_csv_transactions_success():
    """Позитивный тест: проверка корректности возврата данных из CSV."""
    with patch('pandas.read_csv', new_callable=MagicMock) as mock_read_csv:
        mock_read_csv.return_value = create_mock_df()
        result = read_csv_transactions('/path/to/file.csv')
        expected_result = [
            {'id': 650703, 'state': 'EXECUTED', 'date': '2023-09-05T11:30:32Z', 'amount': 16210,
             'currency_name': 'Sol', 'currency_code': 'PEN', 'from': 'Счет 58803664561298323391',
             'to': 'Счет 39745660563456619397', 'description': 'Перевод организации'},
            {'id': 3598919, 'state': 'EXECUTED', 'date': '2020-12-06T23:00:58Z', 'amount': 29740,
             'currency_name': 'Peso', 'currency_code': 'COP', 'from': 'Discover 3172601889670065',
             'to': 'Discover 0720428384694643', 'description': 'Перевод с карты на карту'},
            {'id': 593027, 'state': 'CANCELED', 'date': '2023-07-22T05:02:01Z', 'amount': 30368,
             'currency_name': 'Shilling', 'currency_code': 'TZS', 'from': 'Visa 1959232722494097',
             'to': 'Visa 6804119550473710', 'description': 'Перевод с карты на карту'}
        ]
        assert result == expected_result


def test_read_excel_transactions_success():
    """Позитивный тест: проверка корректности возврата данных из Excel."""
    with patch('pandas.read_excel', new_callable=MagicMock) as mock_read_excel:
        mock_read_excel.return_value = create_mock_df()
        result = read_excel_transactions('/path/to/file.xlsx')
        expected_result = [
            {'id': 650703, 'state': 'EXECUTED', 'date': '2023-09-05T11:30:32Z', 'amount': 16210,
             'currency_name': 'Sol', 'currency_code': 'PEN', 'from': 'Счет 58803664561298323391',
             'to': 'Счет 39745660563456619397', 'description': 'Перевод организации'},
            {'id': 3598919, 'state': 'EXECUTED', 'date': '2020-12-06T23:00:58Z', 'amount': 29740,
             'currency_name': 'Peso', 'currency_code': 'COP', 'from': 'Discover 3172601889670065',
             'to': 'Discover 0720428384694643', 'description': 'Перевод с карты на карту'},
            {'id': 593027, 'state': 'CANCELED', 'date': '2023-07-22T05:02:01Z', 'amount': 30368,
             'currency_name': 'Shilling', 'currency_code': 'TZS', 'from': 'Visa 1959232722494097',
             'to': 'Visa 6804119550473710', 'description': 'Перевод с карты на карту'}
        ]
        assert result == expected_result


def test_read_csv_transactions_failure():
    """Негативный тест: проверка реакции на отсутствующий файл CSV."""
    with unittest.mock.patch('pandas.read_csv', side_effect=FileNotFoundError()):
        with pytest.raises(ValueError):
            read_csv_transactions('/nonexistent/path/to/file.csv')


def test_read_excel_transactions_failure():
    """Негативный тест: проверка реакции на отсутствующий файл Excel."""
    with unittest.mock.patch('pandas.read_excel', side_effect=FileNotFoundError()):
        with pytest.raises(ValueError):
            read_excel_transactions('/nonexistent/path/to/file.xlsx')


if __name__ == '__main__':
    unittest.main()
