# Мои модули
from modules.parsing import get_temperature_for_day
from modules.datetime_tools import get_str_from_datetime, get_datetime_from_str
from modules.errors_and_types import DateDoesNotExist
# Внешние модули
from datetime import datetime
from typing import Tuple
import re
from urllib.error import HTTPError


def input_data() -> Tuple[datetime, datetime]:
    print('Вводите даты в формате дд.мм.гг чч')
    while True:
        dates = []
        for inp_str in ['Начальная дата',  'Конечная дата']:
            while True:
                date_str = input(inp_str)
                try:
                    date = get_datetime_from_str(date_str)
                except ValueError:
                    print('Неверная дата, попробуйте снова')
                else:
                    dates.append(date)
                    break
        start_date, end_date = dates

        if not(start_date <= end_date):
            print('Начальная дата больше конечной, попробуйте снова')
            continue

        for date in [start_date, end_date]:
            try:
                get_temperature_for_day(date)
            except HTTPError as e:
                print('Произошла серверная ошибка. Попробуйте ввести другую дату или обратиться к серверу позже')
                print(f'Сообщение об ошибке:\n{e}')
                continue
            except DateDoesNotExist:
                print(f'Информации по дню {get_str_from_datetime(date)} нет, попробуйте другое значение')
                continue
        return (start_date, end_date)


def input_xlsx_name() -> str:
    pattern = '^([^\S\r\n]|([\d\w()_-]))+$'
    regex = re.compile(pattern, (re.ASCII))
    while True:
        xlsx_name = input('Введите имя таблицы для сохранения без .xlsx: ')
        if regex.search(xlsx_name):
            return xlsx_name + '.xlsx'
        else:
            print('Введено не верное имя!')
