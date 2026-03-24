from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info):
    """Маскирует номер счета или карты в зависимости от входной строки."""
    # Очищаем строку от пробельных символов
    clean_info = info.strip()

    # Если строка пустая после очистки, сразу возвращаем пустую строку
    if not clean_info:
        return ""

    # Проверяем, содержит ли строка хотя бы одну цифру
    if not any(char.isdigit() for char in clean_info):
        return clean_info  # Если цифр нет, возвращаем исходную строку без изменений

    # Если в строке содержится слово "Счет", применяем маску для счета
    if 'Счет' in clean_info:
        return get_mask_account(clean_info)
    else:
        # Иначе считаем, что это карта, и применяем маску для карты
        return get_mask_card_number(clean_info)


# Примеры использования
if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))  # Пример для карты
    print(mask_account_card("Счет 73654108430135874305"))      # Пример для счета


def get_date(date_str):
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
