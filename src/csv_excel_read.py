import pandas as pd


def read_csv_transactions(file_path):
    """
    Функция для считывания финансовых операций из CSV-файла с точкой с запятой ';' в качестве разделителя.

    Параметры:
        file_path (str): Полный путь к файлу CSV.

    Возвращает:
        list of dicts: Список словарей, каждый словарь представляет одну строку с транзакцией.
    """
    try:
        df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')
        return df.to_dict('records')
    except Exception as e:
        raise ValueError(f"Ошибка при чтении CSV-файла {file_path}: {e}")


def read_excel_transactions(file_path):
    """
    Функция для считывания финансовых операций из Excel-файла.

    Параметры:
        file_path (str): Полный путь к файлу Excel.

    Возвращает:
        list of dicts: Список словарей, каждый словарь представляет одну строку с транзакцией.
    """
    try:
        df = pd.read_excel(file_path)
        return df.to_dict('records')
    except Exception as e:
        raise ValueError(f"Ошибка при чтении Excel-файла {file_path}: {e}")


# Демонстрационный запуск функций (только при прямом выполнении модуля)
if __name__ == "__main__":
    # Укажите здесь ваши реальные пути к файлам
    csv_file_path = r"C:\pythonlesson\homework_10_1\transactions.csv"
    excel_file_path = r"C:\pythonlesson\homework_10_1\transactions_excel.xlsx"

    # Проверяем работу функций на примере конкретных файлов
    try:
        csv_transactions = read_csv_transactions(csv_file_path)
        print("Данные из CSV-файла:", csv_transactions[:5])

        excel_transactions = read_excel_transactions(excel_file_path)
        print("\nДанные из Excel-файла:", excel_transactions[:5])
    except Exception as e:
        print(e)
