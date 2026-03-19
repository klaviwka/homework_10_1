# csv/csv_excel_read.py

import pandas as pd
import os

# Описание пути к данным относительно текущего каталога проекта
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Поднимаемся на два уровня вверх
DATA_DIR = os.path.join(ROOT_DIR, 'data')


def read_csv_transactions():
    """
    Читает финансовые операции из CSV-файла.
    """
    file_path = os.path.join(DATA_DIR, 'transactions.csv')

    try:
        df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')
        return df.to_dict('records')
    except Exception as e:
        raise ValueError(f"Ошибка при чтении CSV-файла {file_path}: {e}")


def read_excel_transactions():
    """
    Читает финансовые операции из Excel-файла.
    """
    file_path = os.path.join(DATA_DIR, 'transactions_excel.xlsx')

    try:
        df = pd.read_excel(file_path)
        return df.to_dict('records')
    except Exception as e:
        raise ValueError(f"Ошибка при чтении Excel-файла {file_path}: {e}")