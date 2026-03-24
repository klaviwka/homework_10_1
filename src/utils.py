# src/utils.py

import json
import logging
import os

# Настраиваем логирование
logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs/utils.log"),  # Путь к логам относительно модуля
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def load_operations(file_path):
    """
    Загружает операции из указанного JSON-файла и возвращает список операций.
    """
    if not os.path.isfile(file_path):
        logger.warning(f"Файл {file_path} не существует.")
        return []

    try:
        with open(file_path, mode="r", encoding="utf-8") as file:
            operations = json.load(file)
            if isinstance(operations, list):
                logger.info("Операции успешно загружены из файла %s.", file_path)
                return operations
            else:
                logger.error("Неправильный формат данных в файле %s.", file_path)
                return []
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден.")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка при разборе JSON в файле {file_path}: {e}.")
        return []
    except Exception as e:
        logger.error(f"Произошла ошибка при обработке файла {file_path}: {e}.")
        return []