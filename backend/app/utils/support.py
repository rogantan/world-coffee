"""Вспомогательные функции"""

import calendar
import datetime


def compare_dicts(dict1: dict, dict2: dict) -> bool:
    """Функция сравнения двух словарей"""

    # Проверяем, имеют ли словари одинаковые ключи
    if sorted(dict1.keys()) != sorted(dict2.keys()):
        return False

    # Проверяем значения для каждого ключа
    for key in dict1:
        value1 = dict1[key]
        value2 = dict2[key]

        # Если значения - словари, вызываем эту же функцию рекурсивно
        if isinstance(value1, dict) and isinstance(value2, dict):
            if not compare_dicts(value1, value2):
                return False
        # Если значения - списки, сравниваем их элементы
        elif isinstance(value1, list) and isinstance(value2, list):
            if len(value1) != len(value2):
                return False

            for item1, item2 in zip(
                sorted(value1, key=str), sorted(value2, key=str)
            ):
                # Если элементы - словари, вызываем эту же функцию рекурсивно
                if isinstance(item1, dict) and isinstance(item2, dict):
                    if not compare_dicts(item1, item2):
                        return False
                elif item1 != item2:
                    return False
        elif not isinstance(value1, type(value2)):
            return False
        else:
            # Для всех остальных случаев просто сравниваем значения
            if value1 != value2:
                return False

    return True


def get_month_range(date_from, date_to):
    """Генератор месяцев в указанном диапазоне"""
    date_from = date_from.replace(day=1)
    date_to = date_to.replace(day=1)
    while date_from <= date_to:
        yield date_from

        date_from = (date_from + datetime.timedelta(days=32)).replace(day=1)


def to_month_year_format(date):
    """Приведение даты к формату 'Январь 2024'"""
    months = [
        "Январь",
        "Февраль",
        "Март",
        "Апрель",
        "Май",
        "Июнь",
        "Июль",
        "Август",
        "Сентябрь",
        "Октябрь",
        "Ноябрь",
        "Декабрь",
    ]
    return f"{months[date.month - 1]} {date.year}"


def get_date_from(date_from, date) -> str:
    if date.date() > date_from:
        date_from = date
    return f"{date_from.strftime('%d.%m.%Y')}"


def get_date_to(date_to, date) -> str:
    if date.month != date_to.month:
        date_to = date.replace(
            day=calendar.monthrange(date.year, date.month)[1]
        )
    return f"{date_to.strftime('%d.%m.%Y')}"
