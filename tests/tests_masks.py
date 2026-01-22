import pytest
from src.masks import get_mask_card_number, get_mask_account


@pytest.mark.parametrize("card_number, expected_masked", [
    (7000792289606361, "7000 79** **** 6361"),
    (1234567812345678, "1234 56** **** 5678"),
    (9876543210123456, "9876 54** **** 3456"),
    (1111222233334444, "1111 22** **** 4444"),
    (4000123456789010, "4000 12** **** 9010"),
])
def test_get_mask_card_number(card_number, expected_masked):
    assert get_mask_card_number(card_number) == expected_masked


@pytest.mark.parametrize("card_account, expected_masked", [
    ("73654108430135874305", "**4305"),  # Ожидаемое значение
    ("12345678901234567890", "**7890"),
    ("9876543210", "**3210"),
    ("1111222233334444", "**4444"),
    ("4000123456789010", "**9010"),
])
def test_get_mask_account(card_account, expected_masked):
    assert get_mask_account(card_account) == expected_masked


@pytest.fixture
def card_accounts():
    """Фикстура для предоставления различных номеров счетов."""
    return [
        ("73654108430135874305", "**4305"),
        ("12345678901234567890", "**7890"),
        ("9876543210", "**3210"),
        ("1111222233334444", "**4444"),
        ("4000123456789010", "**9010"),
        (73654108430135874305, "**4305"),  # Тест с целым числом
    ]


def test_get_mask_account_with_fixture(card_accounts):
    """Тестирование функции get_mask_account с использованием фикстуры."""
    for card_account, expected_masked in card_accounts:
        assert get_mask_account(card_account) == expected_masked
