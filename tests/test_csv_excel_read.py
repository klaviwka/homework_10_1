# test_csv_excel_read.py

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.csv_excel_read import read_csv_transactions, read_excel_transactions
import pytest  # добавляем подключение pytest

def create_mock_df():
    """Создание фиктивного DataFrame"""
    return pd.DataFrame({
        'id': [1, 2],
        'state': ['active', 'pending'],
        'date': ['2023-01-01', '2023-01-02'],
        'amount': [100.0, 200.0],
        'currency_name': ['USD', 'EUR'],
        'currency_code': ['USD', 'EUR'],
        'from': ['Account A', 'Account B'],
        'to': ['Account C', 'Account D'],
        'description': ['Transaction 1', 'Transaction 2']
    })

def test_read_csv_transactions_success():
    """Позитивный тест: проверка корректности возврата данных из CSV."""
    with patch('pandas.read_csv', new_callable=MagicMock) as mock_read_csv:
        mock_read_csv.return_value = create_mock_df()
        result = read_csv_transactions('/path/to/file.csv')
        expected_result = [
            {'id': 1, 'state': 'active', 'date': '2023-01-01', 'amount': 100.0,
             'currency_name': 'USD', 'currency_code': 'USD', 'from': 'Account A',
             'to': 'Account C', 'description': 'Transaction 1'},
            {'id': 2, 'state': 'pending', 'date': '2023-01-02', 'amount': 200.0,
             'currency_name': 'EUR', 'currency_code': 'EUR', 'from': 'Account B',
             'to': 'Account D', 'description': 'Transaction 2'}
        ]
        assert result == expected_result

def test_read_excel_transactions_success():
    """Позитивный тест: проверка корректности возврата данных из Excel."""
    with patch('pandas.read_excel', new_callable=MagicMock) as mock_read_excel:
        mock_read_excel.return_value = create_mock_df()
        result = read_excel_transactions('/path/to/file.xlsx')
        expected_result = [
            {'id': 1, 'state': 'active', 'date': '2023-01-01', 'amount': 100.0,
             'currency_name': 'USD', 'currency_code': 'USD', 'from': 'Account A',
             'to': 'Account C', 'description': 'Transaction 1'},
            {'id': 2, 'state': 'pending', 'date': '2023-01-02', 'amount': 200.0,
             'currency_name': 'EUR', 'currency_code': 'EUR', 'from': 'Account B',
             'to': 'Account D', 'description': 'Transaction 2'}
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
