# src/csv_excel_read.py

import pandas as pd
from typing import List, Dict

def read_csv_transactions(file_path: str) -> List[Dict]:
    """
    Читает финансовые операции из CSV-файла по указанному пути.
    """
    try:
        # Используем переданный путь к файлу
        df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')
        return df.to_dict('records')
    except Exception as e:
        raise ValueError(f"Ошибка при чтении CSV-файла {file_path}: {e}")


def read_excel_transactions(file_path: str) -> List[Dict]:
    """
    Читает финансовые операции из Excel-файла по указанному пути.
    """
    try:
        # Используем переданный путь к файлу
        df = pd.read_excel(file_path)
        return df.to_dict('records')
    except Exception as e:
        raise ValueError(f"Ошибка при чтении Excel-файла {file_path}: {e}")
