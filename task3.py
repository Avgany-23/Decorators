"""
Применить написанный логгер к приложению из любого предыдущего д/з.
"""

from typing import Iterable, List, Generator, Any


# ------------------------------ Вызов через первый декоратор ------------------------------

from task1 import logger


@logger
def flat_generator1(list_of_list: List[Iterable]) -> Generator[List[Any], None, None]:
    """Функция-генератор для распаковки вложенных списков"""

    for el in list_of_list:
        if not isinstance(el, list):
            yield el
        else:
            yield from flat_generator1(el)


list_of_lists1 = [
    [['a'], ['b', 'c']],
    ['d', 'e', [['f'], 'h'], False],
    [1, 2, None, [[[[['!']]]]], []]
]

# ------------------------------ Вызов через второй декоратор ------------------------------

from task2 import logger


@logger('generator_log.log')
def flat_generator2(list_of_list: List[Iterable]) -> Generator[List[Any], None, None]:
    """Функция-генератор для распаковки вложенных списков"""

    for el in list_of_list:
        if not isinstance(el, list):
            yield el
        else:
            yield from flat_generator2(el)


list_of_lists2 = [
    [['a'], ['b', 'c']],
    ['d', 'e', [['f'], 'h'], False],
    [1, 2, None, [[[[['!']]]]], []]
]


if __name__ == '__main__':
    generator_list1 = flat_generator1(list_of_lists1)
    generator_list2 = flat_generator2(list_of_lists2)