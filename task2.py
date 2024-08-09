"""
Доработать параметризованный декоратор logger в коде ниже. Должен получиться декоратор,
который записывает в файл дату и время вызова функции, имя функции, аргументы, с которыми вызвалась,
и возвращаемое значение. Путь к файлу должен передаваться в аргументах декоратора.
Функция test_2 в коде ниже также должна отработать без ошибок.
"""


from typing import Callable, Any
from datetime import datetime
import functools
import os


def logger_func(path: str, func: Callable, result: Any, count: int, *args, **kwargs) -> None:

    args_ = ", ".join(map(str, args))
    kwargs_ = ", ".join(f'{key}={kwargs[key]}' for key in kwargs)
    default_args = ", ".join(map(str, func.__defaults__ or []))

    data = (f'Filename function call : {__name__}\n'
            f'Time call: {datetime.now()}\n'
            f'Call {count=}\n'  # Количество вызовов одной и той же функции
            f'--> Name function: {func.__name__}\n'
            f'Returned value: {result or "no result"}\n'
            f'Doc function: {func.__doc__ or "no documentation"}\n'
            f'Defaults arguments: {default_args or "no default"}\n'
            f'- positional arguments: {args_ or "no arguments"}\n'
            f'- Named arguments: {kwargs_ or "no arguments"}\n{"-"*100}\n\n')

    with open(path, 'a', encoding='utf-8') as f:
        f.write(data)


def logger(path: str) -> Callable:
    def __logger(func: Callable) -> Any:
        count = 0

        @functools.wraps(func)
        def new_function(*args, **kwargs) -> Any:
            nonlocal count
            count += 1
            result = func(*args, **kwargs)
            logger_func(path, func, result, count, *args, **kwargs)

            return result

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)


        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()