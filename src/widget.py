from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Маскирует номер счета или карты в зависимости от входной строки."""
    number = info.split()[-1]

    if 'Счет' in info:
        return get_mask_account(number)  # Передаем номер счета в виде строки
    else:
        return get_mask_card_number(number)  # Передаем номер карты в виде строки


# Примеры использования
if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))  # Пример для карты
    print(mask_account_card("Счет 73654108430135874305"))      # Пример для счета


def get_date(date_str: str) -> str:
    """Преобразует строку с датой из формата 'YYYY-MM-DDTHH:MM:SS.ssssss' в формат 'DD.MM.YYYY'."""
    # Парсим входную строку в объект datetime
    date_object = datetime.fromisoformat(date_str)
    # Форматируем дату в нужный формат
    return date_object.strftime("%d.%m.%Y")


# Пример использования
if __name__ == "__main__":
    date_input = "2024-03-11T02:26:18.671407"
    formatted_date = get_date(date_input)
    print(formatted_date)  # Вывод: 11.03.2024
