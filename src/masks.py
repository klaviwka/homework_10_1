import logging

# Настройка логирования
logging.basicConfig(
    filename='./logs/masks.log',  # Исправлено название файла логов
    filemode='w',  # Перезапись файла при каждом запуске
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def get_mask_card_number(card_number: int) -> str:
    """
    Маскирует номер кредитной карты, оставляя видимыми только первые 6 и последние 4 цифры.

    Args:
        card_number (int): Номер кредитной карты в виде целого числа.

    Returns:
        str: Маскированный номер карты в формате 'XXXX XX** **** XXXX'.
    """
    try:
        # Преобразуем целое число в строку
        card_number_str = str(card_number)

        # Маскируем номер карты
        masked_number = f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"

        # Логируем успешное маскирование номера карты
        logging.info(f'Карточка успешно замаскирована: {masked_number}')

        return masked_number
    except Exception as e:
        # Логируем ошибку при обработке номера карты
        logging.error(f'Ошибка при маскировании карточки: {e}')
        raise


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
    try:
        # Преобразуем целое число в строку, если это необходимо
        if isinstance(card_account, int):
            card_account = str(card_account)

        # Маскируем номер счета
        masked_account = f"**{card_account[-4:]}"

        # Логируем успешное маскирование номера счета
        logging.info(f'Номер счёта успешно замаскирован: {masked_account}')

        return masked_account
    except Exception as e:
        # Логируем ошибку при обработке номера счета
        logging.error(f'Ошибка при маскировании номера счёта: {e}')
        raise


# Пример использования
card_account_int = 73654108430135874305
masked_account_int = get_mask_account(card_account_int)
print(masked_account_int)  # Вывод: **4305
