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
        # Открываем файл в режиме 'r' (только чтение)
        with open(file_path, mode="r", encoding="utf-8") as file:
            # Используем json.load() для прямого чтения JSON из файла
            operations = json.load(file)
            if isinstance(operations, list):
                return operations
            else:
                return []
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка при разборе JSON в файле {file_path}: {e}.")
        return []
    except Exception as e:
        print(f"Произошла ошибка при обработке файла {file_path}: {e}.")
        return []
