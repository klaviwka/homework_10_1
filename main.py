import os
import sys
import json
import csv
import openpyxl
from datetime import datetime
from typing import List, Dict
from src.processing import filter_by_state, sort_by_date, process_bank_search, process_bank_operations
import re


def load_json_file(file_path: str) -> List[Dict]:
    """Загружает файл JSON."""
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def load_csv_file(file_path: str, delimiter=",") -> List[Dict]:
    """Загружает файл CSV с указанным разделителем."""
    records = []
    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=delimiter)
        for row in reader:
            records.append(row)
    return records


def load_xlsx_file(file_path: str) -> List[Dict]:
    """Загружает файл Excel (.xlsx)."""
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1]]
    rows = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        rows.append(dict(zip(headers, row)))
    return rows


def validate_status(status: str) -> bool:
    """Проверяет валидный статус транзакции."""
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    return status.upper() in valid_statuses


def prompt_user_choice(prompt: str, choices: List[str]) -> str:
    """Запрашивает у пользователя один из допустимых вариантов."""
    while True:
        choice = input(prompt).upper().strip()
        if choice not in choices:
            print(f"Введённое значение '{choice}' некорректно.")
        else:
            break
    return choice


def display_transaction(transaction: Dict):
    """Форматирует и выводит одну транзакцию."""
    date_str = datetime.strptime(transaction["date"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
    description = transaction['description']

    # Получаем поля FROM и TO
    from_info = transaction.get('from', '')
    to_info = transaction.get('to', '')

    # Функция для правильной маски номера карты/счета
    masked_from = mask_card_or_account_number(from_info)
    masked_to = mask_card_or_account_number(to_info)

    # Получаем сумму и валюту
    amount = float(transaction["operationAmount"]["amount"])
    currency_code = transaction["operationAmount"]["currency"]["code"]
    currency = "руб." if currency_code == "RUB" else currency_code

    # Выводим результат
    print(f"{date_str} {description}")
    if masked_from:  # Если есть отправитель, показываем его
        print(f"<-- {masked_from}")  # Стрелочка показывает направление отправки
    print(f"-> {masked_to}")
    print(f"Сумма: {amount:.2f} {currency}\n")


def mask_card_or_account_number(number: str) -> str:
    """Корректная маска для кредитных карт и банковских счетов."""
    parts = re.findall(r'\w+', number)  # Извлекаем группы численно-буквенных элементов
    masked_parts = []

    for part in parts:
        if part.isdigit():  # Если группа состоит только из цифр
            if len(part) >= 16:  # Маска для банковской карты
                first_four = part[:4]
                last_four = part[-4:]
                masked_part = f"{first_four} {'*' * 6} {'*' * 4} {last_four}"
            elif len(part) > 4:  # Маска для банковского счёта (более 4-х цифр)
                masked_part = f"{'*' * (len(part) - 4)}{part[-4:]}"
            else:  # Короткий счёт (менее 5 цифр)
                masked_part = f"**{part[-2:]}"
        else:  # Группа содержит буквы или спецсимволы
            masked_part = part  # Не маскируем

        masked_parts.append(masked_part)

    return ' '.join(masked_parts)


def apply_keyword_filter(transactions: List[Dict], keyword: str) -> List[Dict]:
    """Фильтрует транзакции по наличию указанного слова в описании."""
    return [tr for tr in transactions if keyword.lower() in tr['description'].lower()]


def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n")
    menu_items = {
        "1": ("Получить информацию о транзакциях из JSON-файла", ".json"),
        "2": ("Получить информацию о транзакциях из CSV-файла", ".csv"),
        "3": ("Получить информацию о транзакциях из XLSX-файла", ".xlsx")
    }

    while True:
        print("Выберите необходимый пункт меню:")
        for k, v in menu_items.items():
            print(f"{k}. {v[0]}")
        user_input = input("Ваш выбор: ").strip()
        if user_input in menu_items.keys():
            _, ext = menu_items[user_input]
            break
        else:
            print("Неверный выбор пункта меню!")

    # Определяем путь относительно исполняемого файла
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_paths = {
        ".json": os.path.join(base_dir, "data", "operations.json"),
        ".csv": os.path.join(base_dir, "data", "transactions.csv"),
        ".xlsx": os.path.join(base_dir, "data", "transactions_excel.xlsx")
    }

    full_path = file_paths.get(ext)

    # Загрузка файлов разных форматов
    try:
        if ext == ".json":
            data = load_json_file(full_path)
        elif ext == ".csv":
            data = load_csv_file(full_path)
        elif ext == ".xlsx":
            data = load_xlsx_file(full_path)
        else:
            raise ValueError("Неправильный тип файла")

        print(f"\nДля обработки выбран {menu_items[user_input][0]}\n")

    except FileNotFoundError:
        print(f"Файл {full_path} не найден.")
        sys.exit(1)

    # Выбор статуса
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    status = None

    while status is None or not validate_status(status):
        status = input("Введите статус, по которому необходимо выполнить фильтрацию "
                       "(доступные статусы: EXECUTED, CANCELED, PENDING): ").strip().upper()
        if not validate_status(status):
            print(f"Статус операции \"{status}\" недоступен.")

    # Фильтруем операции по выбранному статусу
    filtered_data = filter_by_state(data, status)

    # Сообщаем пользователю, что произошло фильтрование
    print(f"\nОперации отфильтрованы по статусу \"{status}\"\n")

    # Проверка наличия транзакций
    if len(filtered_data) == 0:
        print(f"\nПо указанному статусу \"{status}\" не найдены соответствующие операции.")
        exit()

    # Предложение сортировки по дате
    sorting_needed = prompt_user_choice("Отсортировать операции по дате? (Да/Нет): ", ["ДА", "НЕТ"])
    if sorting_needed == "ДА":
        ascending = prompt_user_choice("Отсортировать по возрастанию или по убыванию?: ",
                                       ["ПО ВОЗРАСТАНИЮ", "ПО УБЫВАНИЮ"])

        # Устанавливаем порядок сортировки
        sort_order = ascending == "ПО ВОЗРАСТАНИЮ"
        filtered_data = sort_by_date(filtered_data, descending=(not sort_order))

    # Далее проверяем, нужны ли только рублевые транзакции
    ruble_filter = prompt_user_choice("Выводить только рублевые транзакции? (Да/Нет): ", ["ДА", "НЕТ"])
    if ruble_filter == "ДА":
        filtered_data = [
            item for item in filtered_data
            if item["operationAmount"]["currency"]["code"] == "RUB"
        ]

    # Поиск по ключевому слову в описании
    search_word = prompt_user_choice(
        "Отфильтровать список транзакций по определенному слову в описании? (Да/Нет): ",
        ["ДА", "НЕТ"]
    )
    if search_word == "ДА":
        keyword = input("Введите слово для поиска: ")
        filtered_data = apply_keyword_filter(filtered_data, keyword)

    # Вывод всех транзакций
    if len(filtered_data) == 0:
        print("\nНе найдено ни одной транзакции, соответствующей вашим условиям фильтрации.")
    else:
        print(f"\nВсего банковских операций в выборке: {len(filtered_data)} шт.\n")
        for idx, tr in enumerate(filtered_data):
            display_transaction(tr)


if __name__ == "__main__":
    main()
