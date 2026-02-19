# tests/test_external_api.py

from unittest.mock import patch, Mock
from src.external_api import convert_transaction_to_rubles


def test_convert_usd_to_rubles_successfully():
    """Тест успешного конвертирования суммы из USD в рубли"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 7500.00}  # Обратите внимание на ключ "result"

    with patch('requests.get', return_value=mock_response):
        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "USD"
                }
            }
        }

        expected_result = 7500.00
        actual_result = convert_transaction_to_rubles(transaction)
        assert actual_result == expected_result


def test_convert_eur_to_rubles_successfully():
    """Тест успешного конвертирования суммы из EUR в рубли"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": 4250.00}  # Обратите внимание на ключ "result"

    with patch('requests.get', return_value=mock_response):
        transaction = {
            "operationAmount": {
                "amount": "50.00",
                "currency": {
                    "code": "EUR"
                }
            }
        }

        expected_result = 4250.00
        actual_result = convert_transaction_to_rubles(transaction)
        assert actual_result == expected_result


def test_return_original_amount_if_rubles():
    """Тест, что функция возвращает изначальную сумму, если валюта уже рубли"""
    transaction = {
        "operationAmount": {
            "amount": "3000.00",
            "currency": {
                "code": "RUB"
            }
        }
    }

    result = convert_transaction_to_rubles(transaction)
    assert result == 3000.00


def test_raise_exception_on_unsupported_currency():
    """Тест, что функция поднимает исключение при неизвестной валюте"""
    transaction = {
        "operationAmount": {
            "amount": "100.00",
            "currency": {
                "code": "BTC"
            }
        }
    }

    try:
        convert_transaction_to_rubles(transaction)
    except ValueError:
        pass
    else:
        raise AssertionError("Ожидалось исключение ValueError")


def test_raise_exception_on_api_failure():
    """Тест, что функция поднимает исключение при отказе API"""
    mock_response = Mock()
    mock_response.status_code = 404

    with patch('requests.get', return_value=mock_response):
        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "USD"
                }
            }
        }

        try:
            convert_transaction_to_rubles(transaction)
        except RuntimeError:
            pass
        else:
            raise AssertionError("Ожидалось исключение RuntimeError")
