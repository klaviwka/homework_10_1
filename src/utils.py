# src/utils.py

import json
import os


def load_operations(file_path):
    """
    Загружает операции из указанного JSON-файла и возвращает список операций.

    :param file_path: Полный путь к файлу с операциями.
    :return: Список словарей с операциями или пустой список, если файл некорректен.
    """
    if not os.path.isfile(file_path):
        return []

    try:
        with open(file_path, encoding='utf-8') as file:
            data = file.read()  # Чтение файла целиком
            operations = json.loads(data)  # Парсинг JSON
            if isinstance(operations, list):
                return operations
            else:
                return []
    except Exception as e:
        print(f"Произошла ошибка при обработке файла {file_path}: {e}")
        return []
