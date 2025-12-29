import pytest
from src.masks import get_mask_card_number, get_mask_account


# Тесты для функции get_mask_card_number
@pytest.mark.parametrize("input_card, expected_output", [
    ("7000792289606361", "7000 79** **** 6361"),  # Изменено на строку
    ("1234567890123456", "1234 56** **** 3456"),  # Изменено на строку
    ("9876543210123456", "9876 54** **** 3456"),  # Изменено на строку
])
def test_get_mask_card_number(input_card: str, expected_output: str) -> None:
    assert get_mask_card_number(input_card) == expected_output


# Тесты для функции get_mask_account
@pytest.mark.parametrize("input_account, expected_output", [
    ("73654108430135874305", "**4305"),
    ("12345678901234567890", "**7890"),
])
def test_get_mask_account(input_account: str, expected_output: str) -> None:
    assert get_mask_account(input_account) == expected_output


# Запуск тестов
if __name__ == "__main__":
    pytest.main()
