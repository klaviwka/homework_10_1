def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер кредитной карты, оставляя видимыми только первые 6 и последние 4 цифры.

    Args:
        card_number (str): Номер кредитной карты в виде строки.

    Returns:
        str: Маскированный номер карты в формате 'XXXX XX** **** XXXX'.
    """
    masked_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return masked_number

def get_mask_account(card_account: str) -> str:
    """
    Маскирует номер счета, оставляя видимыми только последние 4 цифры.

    Args:
        card_account (str): Номер счета в виде строки.

    Returns:
        str: Маскированный номер счета в формате '**XXXX', где XXXX - последние 4 цифры.
    """
    masked_account = f"**{card_account[-4:]}"
    return masked_account
