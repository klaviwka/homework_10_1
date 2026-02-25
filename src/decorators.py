from functools import wraps
import datetime


def log(filename=None):
    """
    Логирующий декоратор, который регистрирует успешность выполнения функции либо возникающую ошибку.

    Параметры:
        filename (str): Имя файла для сохранения журнала операций. Если не указано, выводится в консоль.

    Возвращаемое значение:
        function: Обертка вокруг декорированной функции, обеспечивающая журналирование.
    """

    def decorator(func):
        """
        Внутренний декоратор, применяемый непосредственно к целевой функции.

        Параметры:
            func (callable): Функциональная единица, подлежащая регистрации действий.

        Возвращаемое значение:
            callable: Замещённая версия оригинальной функции с возможностью журналирования.
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            """
            Обёртка над исходной функцией, выполняющая регистрацию начала и окончания выполнения функции.

            Параметры:
                *args: Позиционные аргументы функции.
                **kwargs: Именованные аргументы функции.

            Возвращаемое значение:
                Любой тип: Результат выполнения исходной функции.

            Возможные исключения:
                Exception: Любое возникшее исключение передается дальше с регистрацией в журнале.
            """
            start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                result = func(*args, **kwargs)
                end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = (
                    f"[{start_time}] Function '{func.__name__}' executed successfully "
                    f"at [{end_time}]. Result: {result}\n"
                )
                if filename is not None:
                    with open(filename, 'a') as file:
                        file.write(message)
                else:
                    print(message.strip())
                return result
            except Exception as e:
                input_params = (
                    f"({', '.join(map(str, args))}), {{"
                    f"{', '.join([f'{k}: {v}' for k, v in kwargs.items()])}}}"
                    if len(kwargs) > 0
                    else f"({', '.join(map(str, args))})"
                )
                error_message = (
                    f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"Function '{func.__name__}' raised an exception: {type(e).__name__}. "
                    f"Inputs: {input_params}\n"
                )
                if filename is not None:
                    with open(filename, 'a') as file:
                        file.write(error_message)
                else:
                    print(error_message.strip())
                raise  # Передача исключения далее по цепочке

        return wrapper

    return decorator


# Пример использования:
@log(filename="mylog.txt")
def my_function(x, y):
    """
    Простая демонстрационная функция, суммирующая два аргумента.

    Параметры:
        x (int): Первый аргумент.
        y (int): Второй аргумент.

    Возвращаемое значение:
        int: Сумма аргументов.
    """
    return x + y


try:
    my_function(1, 2)
except Exception as err:
    print("Error occurred:", str(err))
