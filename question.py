from logging.handlers import RotatingFileHandler
from typing import Callable, Any
import functools
import logging
import os


def logger(path):
    def loggers(func: Callable[..., Any]) -> Callable:
        count = 0

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)
            nonlocal count
            count += 1

            # ------ Create logs -------
            logger = logging.getLogger(__name__)
            logger.setLevel(logging.DEBUG)

            """
            В обоих вариантах файлы записываются криво.
            """
            # ------------------------- ПЕРВЫЙ ВАРИАНТ ЗАПИСИ -------------------------
            # logging.basicConfig(level=logging.DEBUG,
            #                     filename=path,
            #                     filemode='w',
            #                     encoding='utf-8',
            #                     format='Filename function call : %(name)s\n'
            #                            'Time call: %(asctime)s\n'
            #                            'Level log: %(levelname)s\n'
            #                            'Message:\n%(message)s\n')
            # ------------------------------------------------------------------------

            # ------------------------- ВТОРОЙ ВАРИАНТ ЗАПИСИ -------------------------
            handler = RotatingFileHandler(path, encoding='utf-8', mode='a')
            formatter = logging.Formatter('Filename function call : %(name)s\n'
                                          'Time call: %(asctime)s\n'
                                          'Level log: %(levelname)s\n'
                                          'Message:\n%(message)s\n')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            # ------------------------------------------------------------------------



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
    return loggers


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