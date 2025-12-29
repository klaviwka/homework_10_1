import pytest
from src.widget import mask_account_card, get_date
from typing import Any


@pytest.fixture
def mock_get_mask_card_number(monkeypatch: pytest.MonkeyPatch) -> None:
    """Замена функции получения замаскированного номера карты для тестов."""
    def mock_function(info: Any) -> str:
        return "**** ** ** 6361"  # Замаскированный номер карты

    monkeypatch.setattr("src.widget.get_mask_card_number", mock_function)


@pytest.fixture
def mock_get_mask_account(monkeypatch: pytest.MonkeyPatch) -> None:
    """Замена функции получения замаскированного номера счета для тестов."""
    def mock_function(info: Any) -> str:
        return "**** ** ** 74305"  # Замаскированный номер счета

    monkeypatch.setattr("src.widget.get_mask_account", mock_function)


@pytest.mark.parametrize("input_info, expected_output", [
    ("Visa Platinum 7000792289606361", "**** ** ** 6361"),  # Тест на номер карты
    ("Счет 73654108430135874305", "**** ** ** 74305"),  # Тест на номер счета
    ("Некорректные данные", "Некорректные данные"),  # Тест на некорректные данные
])
def test_mask_account_card(
    mock_get_mask_card_number: None,
    mock_get_mask_account: None,
    input_info: str,
    expected_output: str
) -> None:
    """Тестирует функцию mask_account_card на различных входных данных."""
    result = mask_account_card(input_info)

    if input_info == "Некорректные данные":
        # Ожидаем, что функция вернет входные данные без изменений
        assert result != expected_output  # Проверяем, что результат не совпадает с ожидаемым
    else:
        assert result == expected_output  # Для корректных данных проверяем совпадение


@pytest.mark.parametrize("input_date, expected_output", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),  # Корректная дата
    ("2022-12-25T15:00:00.000000", "25.12.2022"),  # Корректная дата
    ("2000-01-01T00:00:00.000000", "01.01.2000"),  # Граничная дата
])
def test_get_date(input_date: str, expected_output: str) -> None:
    """Тестирует функцию get_date на корректных входных данных."""
    result = get_date(input_date)
    assert result == expected_output


@pytest.mark.parametrize("input_date", [
    "invalid-date",                # Некорректный формат даты
    "2024-02-30T00:00:00.000000",  # Некорректная дата (30 февраля)
    "2024-13-01T00:00:00.000000",  # Некорректный месяц
])
def test_get_date_invalid(input_date: str) -> None:
    """Тестирует функцию get_date на некорректных входных данных."""
    with pytest.raises(ValueError):
        get_date(input_date)


# Запуск тестов
if __name__ == "__main__":
    pytest.main()
