import os
import sys
from datetime import datetime
from typing import List, Dict
from src.processing import filter_by_state, sort_by_date, process_bank_search
from src.utils import load_operations
from src.csv_excel_read import read_csv_transactions, read_excel_transactions
from src.masks import get_mask_card_number, get_mask_account

# Меню пунктов выбора файла
MENU_ITEMS = {
    "1": ("Получить информацию о транзакциях из JSON-файла", ".json"),
    "2": ("Получить информацию о транзакциях из CSV-файла", ".csv"),
    "3": ("Получить информацию о транзакциях из XLSX-файла", ".xlsx")
}

# Допустимые статусы операций
VALID_STATUSES = ["EXECUTED", "CANCELED", "PENDING"]

def prompt_user_choice(prompt: str, choices: List[str]):
    """
    Запрашивает у пользователя одно из значений списка choices.
    """
    while True:
        choice = input(prompt).strip().upper()
        if choice not in choices:
            print(f"Введенное значение '{choice}' некорректно.")
        else:
            break
    return choice

def display_transaction(transaction: Dict):
    """
    Показывает отдельную транзакцию в удобочитаемом виде.
    """
    date_str = datetime.strptime(transaction["date"], "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")
    description = transaction['description']

    # Маскируем номер карты или счета
    field_from = transaction.get('from', '')
    field_to = transaction.get('to', '')

    # Маска номеров карт/счетов
    if field_from.isdigit():
        masked_from = get_mask_card_number(field_from)
    else:
        masked_from = get_mask_account(field_from)

    if field_to.isdigit():
        masked_to = get_mask_card_number(field_to)
    else:
        masked_to = get_mask_account(field_to)

    # Получаем сумму и валюту
    amount = float(transaction["operationAmount"]["amount"])
    currency_code = transaction["operationAmount"]["currency"]["code"]
    currency = "руб." if currency_code == "RUB" else currency_code

    # Выводим результат
    print(f"{date_str} {description}")
    if masked_from:
        print(f"Отправитель: {masked_from}")
    if masked_to:
        print(f"Получатель: {masked_to}")
    print(f"Сумма: {amount:.2f} {currency}\n")

def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n")

    # Выбираем тип файла
    while True:
        print("Выберите необходимый пункт меню:")
        for k, v in MENU_ITEMS.items():
            print(f"{k}. {v[0]}")
        user_input = input("Ваш выбор: ").strip()
        if user_input in MENU_ITEMS.keys():
            _, ext = MENU_ITEMS[user_input]
            break
        else:
            print("Неверный выбор пункта меню!")

    # Формирование относительного пути к файлу
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    full_path = os.path.join(data_dir, f'transactions.{ext}') if ext != '.json' else os.path.join(data_dir, 'operations.json')

    # Чтение данных из выбранного файла
    try:
        if ext == ".json":
            data = load_operations(full_path)
        elif ext == ".csv":
            data = read_csv_transactions(full_path)
        elif ext == ".xlsx":
            data = read_excel_transactions(full_path)
        else:
            raise ValueError("Неправильный тип файла")

        print(f"\nДля обработки выбран {MENU_ITEMS[user_input][0]}\n")
    except FileNotFoundError:
        print(f"Файл {full_path} не найден.")
        sys.exit(1)

    # Пользователь вводит статус транзакции
    status = None
    while status is None or status.upper() not in VALID_STATUSES:
        status = input(
            "Введите статус, по которому необходимо выполнить фильтрацию\n(доступные статусы: EXECUTED, CANCELED, PENDING): ").strip().upper()
        if status.upper() not in VALID_STATUSES:
            print(f"Статус операции \"{status}\" недоступен.")

    # Фильтруем операции по введенному статусу
    filtered_data = filter_by_state(data, status)
    print(f"\nОперации отфильтрованы по статусу \"{status}\"\n")

    # Если операция завершилась нулевым результатом
    if len(filtered_data) == 0:
        print(f"\nПо указанному статусу \"{status}\" не найдены соответствующие операции.")
        sys.exit(0)

    # Предлагаем отсортировать операции по дате
    sorting_needed = prompt_user_choice("Отсортировать операции по дате? (Да/Нет): ", ["ДА", "НЕТ"])
    if sorting_needed == "ДА":
        ascending = prompt_user_choice("Отсортировать по возрастанию или по убыванию?: ",
                                       ["ПО ВОЗРАСТАНИЮ", "ПО УБЫВАНИЮ"])
        sort_order = ascending == "ПО ВОЗРАСТАНИЮ"
        filtered_data = sort_by_date(filtered_data, descending=(not sort_order))

    # Дополнительно выводим только рублевые транзакции
    ruble_filter = prompt_user_choice("Выводить только рублевые транзакции? (Да/Нет): ", ["ДА", "НЕТ"])
    if ruble_filter == "ДА":
        filtered_data = [item for item in filtered_data if item["operationAmount"]["currency"]["code"] == "RUB"]

    # Дополнительный фильтр по слову в описании
    search_word = prompt_user_choice("Отфильтровать список транзакций по определенному слову в описании? (Да/Нет): ",
                                     ["ДА", "НЕТ"])
    if search_word == "ДА":
        word_to_search = input("Введите слово для поиска: ")
        filtered_data = process_bank_search(filtered_data, word_to_search)

    # Вывод результатов
    if len(filtered_data) == 0:
        print("\nНе найдено ни одной транзакции, соответствующей вашим условиям фильтрации.")
    else:
        print(f"\nВсего банковских операций в выборке: {len(filtered_data)}\n")
        for idx, tr in enumerate(filtered_data):
            display_transaction(tr)

if __name__ == "__main__":
    main()
