# src/utils.py

import json
import os
import logging

# Настраиваем логирование
logging.basicConfig(
    filename='./logs/utils.log',   # Имя файла логов
    filemode='w',                  # Режим перезаписи
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO            # Уровнем серьёзности INFO будем фиксировать события
)

logger = logging.getLogger(__name__)  # Получаем объект logger для текущего модуля


def load_operations(file_path):
    """
    Загружает операции из указанного JSON-файла и возвращает список операций.

    :param file_path: Полный путь к файлу с операциями.
    :return: Список словарей с операциями или пустой список, если файл некорректен.
    """
    if not os.path.isfile(file_path):
        logger.warning(f"Файл {file_path} не существует.")  # Логируем предупреждение
        return []

    try:
        # Открываем файл в режиме 'r' (только чтение)
        with open(file_path, mode="r", encoding="utf-8") as file:
            # Используем json.load() для прямого чтения JSON из файла
            operations = json.load(file)
            if isinstance(operations, list):
                logger.info("Операции успешно загружены из файла %s.", file_path)  # Логируем успех загрузки
                return operations
            else:
                logger.error("Неправильный формат данных в файле %s.", file_path)  # Логируем неправильный формат даных
                return []
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден.")  # Логируем отсутствие файла
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка при разборе JSON в файле {file_path}: {e}.")  # Логируем ошибку парсинга JSON
        return []
    except Exception as e:
        logger.error(f"Произошла ошибка при обработке файла {file_path}: {e}.")  # Логируем общую ошибку
        return []
