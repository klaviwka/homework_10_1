import os
import re

import pytest
from src.decorators import log


# Пример функции для тестирования
@log(filename="test_log.txt")
def add(x, y):
    return x + y


@log(filename="test_log.txt")
def divide(x, y):
    return x / y  # Деление на ноль вызовет ошибку


def test_function_success_logging():
    result = add(3, 4)
    assert result == 7

    with open("test_log.txt", 'r') as file:
        logs = file.read()
        assert re.search(r"Function 'add' executed successfully", logs)


def test_function_exception_logging():
    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    with open("test_log.txt", 'r') as file:
        logs = file.read()
        assert re.search(r"Function 'divide' raised an exception: ZeroDivisionError", logs)


def test_console_output_when_no_filename(capsys):
    @log()
    def test_function_no_file(x, y):
        return x + y

    test_function_no_file(1, 2)

    captured = capsys.readouterr()
    assert re.search(r"Function 'test_function_no_file' executed successfully", captured.out)


@pytest.fixture(autouse=True)
def cleanup_log_file():
    yield
    # Удаление лог-файла после каждого теста
    try:
        os.remove("test_log.txt")
    except FileNotFoundError:
        pass
