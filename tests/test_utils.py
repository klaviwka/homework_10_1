# tests/test_utils.py

import unittest
from unittest.mock import Mock, patch

from src.utils import load_operations


class FileMock(Mock):
    def __init__(self, content=None):
        super().__init__()
        self.content = content

    def read(self):
        return self.content

    def __enter__(self):
        return self  # Просто возвращаем себя при входе в контекст

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass  # Ничего не делаем при выходе из контекста


@patch('builtins.open')
@patch('os.path.isfile')
def test_load_valid_json(mock_isfile, mock_open):
    """Тестирует успешную загрузку корректного JSON."""
    mock_isfile.return_value = True
    file_mock = FileMock(content='[{"id": 1}]')  # Создаем объект с правильным содержанием
    mock_open.return_value = file_mock

    result = load_operations("/path/to/file.json")
    assert result == [{"id": 1}], f"Результат: {result}, ожидаемый: [{{'id': 1}}]"


@patch('os.path.isfile')
def test_load_nonexistent_file(mock_isfile):
    """Тестирует попытку чтения несуществующего файла."""
    mock_isfile.return_value = False

    result = load_operations("/nonexistent/path.json")
    assert result == [], f"Результат: {result}, ожидаемый: []"


@patch('builtins.open', side_effect=FileNotFoundError)
def test_handle_file_not_found_error(mock_open):
    """Тестирует обработку ситуации отсутствия файла."""
    result = load_operations("/path/to/file.json")
    assert result == [], f"Результат: {result}, ожидаемый: []"


@patch('builtins.open')
@patch('os.path.isfile')
def test_invalid_json_format(mock_isfile, mock_open):
    """Тестирует обработку файла с недействительным форматом JSON."""
    mock_isfile.return_value = True
    file_mock = FileMock(content='{"invalid}')  # Содержимое с недействительным JSON
    mock_open.return_value = file_mock

    result = load_operations("/path/to/file.json")
    assert result == [], f"Результат: {result}, ожидаемый: []"


if __name__ == '__main__':
    unittest.main()
