def get_mask_card_number(card_number: int) -> str:
    """
    Маскирует номер кредитной карты, оставляя видимыми только первые 6 и последние 4 цифры.

    Args:
        card_number (int): Номер кредитной карты в виде целого числа.

    Returns:
        str: Маскированный номер карты в формате 'XXXX XX** **** XXXX'.
    """
    # Преобразуем целое число в строку
    card_number_str = str(card_number)
    # Маскируем номер карты
    masked_number = f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"
    return masked_number

# Пример использования
card_number = 7000792289606361
masked_card = get_mask_card_number(card_number)
print(masked_card)  # Вывод: 7000 79** **** 6361


def get_mask_account(card_account: str) -> str:
    """
    Маскирует номер счета, оставляя видимыми только последние 4 цифры.

    Args:
        card_account (str): Номер счета в виде строки.

    Returns:
        str: Маскированный номер счета в формате '**XXXX', где XXXX - последние 4 цифры.
    """
    # Преобразуем целое число в строку, если это необходимо
    if isinstance(card_account, int):
        card_account = str(card_account)

    # Маскируем номер счета
    masked_account = f"**{card_account[-4:]}"

    return masked_account


# Пример использования
card_account_int = 73654108430135874305
masked_account_int = get_mask_account(card_account_int)
print(masked_account_int)  # Вывод: **4305
