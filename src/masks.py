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
    Маскирует номер кредитной карты, оставляя видимыми первые 4 и 6-ю–7-ю цифры, а также последние 4 цифры.
    Остальные символы заменяются на звёздочки в формате 'XXXX XX** **** XXXX'.

    Args:
        card_number (int): Номер кредитной карты в виде целого числа.

    Returns:
        str: Маскированный номер карты в формате 'XXXX XX** **** XXXX'.
    """
    try:
        card_number_str = str(card_number)
        # Для стандартной карты (16 цифр): XXXX XX** **** XXXX
        masked_number = f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"
        logging.info(f'Карточка успешно замаскирована: {masked_number}')
        return masked_number
    except Exception as e:
        logging.error(f'Ошибка при маскировании карточки: {e}')
        raise


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета, оставляя видимыми только последние 4 цифры.

    Args:
        account_number (str): Номер счета в виде строки.

    Returns:
        str: Маскированный номер счета в формате '**XXXX', где XXXX - последние 4 цифры.
    """
    try:
        # Преобразуем целое число в строку, если это необходимо
        if isinstance(account_number, int):
            account_number = str(account_number)

        # Берём последние 4 цифры и дополняем нулями слева до длины 4 символов
        last_digits = account_number[-4:].zfill(4)

        # Формируем финальную маску
        masked_account = f"**{last_digits}"

        # Логируем успешное маскирование номера счета
        logging.info(f'Номер счёта успешно замаскирован: {masked_account}')

        return masked_account
    except Exception as e:
        # Логируем ошибку при обработке номера счета
        logging.error(f'Ошибка при маскировании номера счёта: {e}')
        raise
