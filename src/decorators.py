from functools import wraps
import datetime


def log(filename=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                result = func(*args, **kwargs)
                end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = f"[{start_time}] Function '{func.__name__}' executed successfully at [{end_time}]. Result: {result}\n"
                if filename is not None:
                    with open(filename, 'a') as file:
                        file.write(message)
                else:
                    print(message.strip())  # выводит в консоль
                return result
            except Exception as e:
                input_params = f"({', '.join(map(str, args))}), {{{', '.join([f'{k}: {v}' for k, v in kwargs.items()])}}}" if len(kwargs) > 0 else f"({', '.join(map(str, args))})"
                error_message = f"[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Function '{func.__name__}' raised an exception: {type(e).__name__}. Inputs: {input_params}\n"
                if filename is not None:
                    with open(filename, 'a') as file:
                        file.write(error_message)
                else:
                    print(error_message.strip())  # выводит в консоль
                raise  # поднимает ошибку обратно вверх по стеку
        return wrapper
    return decorator


# Пример использования:
@log(filename="mylog.txt")
def my_function(x, y):
    return x + y


try:
    my_function(1, 2)
except Exception as err:
    print("Error occurred:", str(err))
