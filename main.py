import csv
import json
import sys
from collections import Counter
from datetime import datetime
from typing import Dict, List

import openpyxl

from src.processing import filter_by_state, process_bank_search, sort_by_date


def load_json_file(file_path: str) -> List[Dict]:
    """Загружает файл JSON."""
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def load_csv_file(file_path: str) -> List[Dict]:
    """Загружает файл CSV."""
    records = []
    with open(file_path, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
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
    to_info = transaction.get('to', '')

    # Функция для правильной маски номера карты/счета
    def mask_number(number):
        if len(number) >= 16 and number.isdigit():  # карточный номер (полностью цифровой и минимум 16 символов)
            first_four = number[:4]
            last_four = number[-4:]
            hidden_middle = "****** ****"
            return f"{first_four} {hidden_middle} {last_four}"
        elif len(number) >= 4 and number.isdigit():  # номер счёта (меньше 16 символов)
            return f"**{number[-4:]}"  # оставляем последние 4 цифры
        return number
    # Применяем маску к полю TO
    to_masked = mask_number(to_info)

    # Получаем сумму и валюту
    amount = float(transaction["operationAmount"]["amount"])
    currency_code = transaction["operationAmount"]["currency"]["code"]
    currency = "руб." if currency_code == "RUB" else currency_code

    # Выводим результат
    print(f"{date_str} {description}")
    print(f"-> {to_masked}")  # Убираем лишнюю стрелочку
    print(f"Сумма: {amount:.2f} {currency}\n")


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Группирует банковские операции по категориям."""
    counter = Counter()
    for record in data:
        if 'description' in record:
            for cat in categories:
                if cat.lower() in record['description'].lower():
                    counter[cat] += 1
    return dict(counter)


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

    # Путь к файлам
    file_paths = {
        ".json": r"C:\pythonlesson\homework_10_1\data\operations.json",
        ".csv": r"C:\pythonlesson\homework_10_1\transactions.csv",
        ".xlsx": r"C:\pythonlesson\homework_10_1\transactions_excel.xlsx"
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

    # Далее проверяем, нужны ли только рублёвые транзакции
    ruble_filter = prompt_user_choice("Выводить только рублёвые транзакции? (Да/Нет): ", ["ДА", "НЕТ"])
    if ruble_filter == "ДА":
        filtered_data = [
            item for item in filtered_data
            if item["operationAmount"]["currency"]["code"] == "RUB"
        ]

    # Поиск по ключевому слову в описании
    search_word = prompt_user_choice(
        "Отфильтровать список транзакций по определённому слову в описании? (Да/Нет): ",
        ["ДА", "НЕТ"]
    )
    if search_word == "ДА":
        word_to_search = input("Введите слово для поиска: ")
        filtered_data = process_bank_search(filtered_data, word_to_search)

    # Вывод всех транзакций
    if len(filtered_data) == 0:
        print("\nНе найдено ни одной транзакции, соответствующей вашим условиям фильтрации.")
    else:
        print(f"\nВсего банковских операций в выборке: {len(filtered_data)} шт.\n")
        for idx, tr in enumerate(filtered_data):
            display_transaction(tr)


if __name__ == "__main__":
    main()
