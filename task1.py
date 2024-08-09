"""
Доработать декоратор logger в коде ниже. Должен получиться декоратор, который записывает в файл 'main.log'
дату и время вызова функции, имя функции, аргументы, с которыми вызвалась, и возвращаемое значение.
Функция test_1 в коде ниже также должна отработать без ошибок.
"""

from typing import Callable, Any
import functools
import logging
import os


def logger(func: Callable[..., Any]) -> Callable:
    count = 0

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        result = func(*args, **kwargs)
        nonlocal count
        count += 1

        # ------ Create logs -------
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG,
                            filename='main.log',
                            filemode='w',
                            encoding='utf-8',
                            format='Filename function call : %(name)s\n'
                                   'Time call: %(asctime)s\n'
                                   'Level log: %(levelname)s\n'
                                   'Message:\n%(message)s\n')

        args_ = ", ".join(map(str, args))
        kwargs_ = ", ".join(f'{key}={kwargs[key]}' for key in kwargs)
        default_args = ", ".join(map(str, func.__defaults__ or []))

        logger.info(f'Call {count=}\n'  # number of call to the same functions
                    f'--> Name function: {func.__name__}\n'
                    f'Returned value: {result or "no result"}\n'
                    f'Doc function: {func.__doc__ or "no documentation"}\n'
                    f'Defaults arguments: {default_args or "no default"}\n'
                    f'- positional arguments: {args_ or "no arguments"}\n'
                    f'- Named arguments: {kwargs_ or "no arguments"}\n{"-"*100}')

        return result
    return wrapper


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()