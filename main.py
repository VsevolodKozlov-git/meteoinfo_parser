import xlsxwriter
from requests import post, get
from urllib.error import  HTTPError
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import List, Tuple
from time import sleep
import re

@dataclass(frozen=True)
class TemperatureData:
    temperature: int
    date: datetime

class DateDoesNotExist(Exception):
    """Ошибка появляющаяся если нет страницы на такой запрос"""

def get_date_str(dt: datetime) -> str:
    return dt.strftime('%d/%m/%y %H:00')

def get_unix_time(dt: datetime) -> int:
    epoch = datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds())


def get_bs_for_date(dt: datetime) -> BeautifulSoup:
    unix_time = get_unix_time(dt)
    params = {'lang': 'ru-RU', 'id_city': 1659, 'dt': unix_time, 'had_db': 1, 'dop': 0}
    url = 'https://meteoinfo.ru/hmc-output/observ/obs_arch.php'
    response = post(url, params=params)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')


def parse_temperature(bs: BeautifulSoup) -> int:
    temperature_list = bs.select('tr:nth-of-type(3) td:nth-of-type(2)')
    if len(temperature_list) == 0:
        raise DateDoesNotExist
    temperature = temperature_list[0].text
    return float(temperature)


def get_temperature_for_day(dt):
    bs = get_bs_for_date(dt)
    temperature = parse_temperature(bs)
    return temperature


def get_temperatures_in_range(start_dt: datetime, end_dt: datetime) -> List[TemperatureData]:
    one_hour_delta = timedelta(hours=1)
    cur_dt = start_dt
    data = []
    while cur_dt <= end_dt:
        date_str = get_date_str(cur_dt)
        try:
           temperature = get_temperature_for_day(cur_dt)
        except HTTPError as e:
            print(f'Серверна ошибка. Дата: f{date_str}')
            print('Сообщение об ошибке:\n')
            print(e)
            continue
        except DateDoesNotExist:
            print(f'Нет данных по дате: {date_str}')
            continue

        data.append(TemperatureData(temperature, cur_dt))
        print(f'Собраны данные для даты {date_str}. Засыпаю на 4 секунды')
        cur_dt += one_hour_delta
        sleep(4)
    return data


def save_to_xlsx(data: List[TemperatureData], xlsx_name) -> None:
    workbook = xlsxwriter.Workbook(xlsx_name+'.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'Дата')
    worksheet.write(0, 1, 'Температура')
    row = 1
    for temperature_data in data:
        dt = temperature_data.date
        temperature = temperature_data.temperature
        date_format = workbook.add_format({'num_format': 'dd/mm/yy hh'})
        worksheet.write_datetime(row, 0, dt, date_format)
        worksheet.write_number(row, 1, temperature)
        row += 1
    workbook.close()


def input_data() -> Tuple[datetime, datetime]:
    print('Вводите даты в формате дд.мм.гг чч')
    while True:
        dates = []
        for inp_str in ['Начальная дата',  'Конечная дата']:
            while True:
                date_str = input(inp_str)
                try:
                    date = datetime.strptime(date_str, '%d.%m.%y %H')
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
                print(f'Информации по дню {get_date_str(date)} нет, попробуйте другое значение')
                continue
        return (start_date, end_date)


def input_xlsx_name() -> str:
    pattern = '^([^\S\r\n]|([\d\w()_-]))+$'
    regex = re.compile(pattern, (re.ASCII))
    while True:
        xlsx_name = input('Введите имя таблицы для сохранения без .xlsx: ')
        if regex.search(xlsx_name):
            return xlsx_name
        else:
            print('Введено не верное имя!')


def main():
    start_dt, end_dt = input_data()
    xlsx_name = input_xlsx_name()
    print('-'*40)
    data = get_temperatures_in_range(start_dt, end_dt)
    save_to_xlsx(data, xlsx_name)
    print('Данные сохранены в таблицу')


if __name__ == '__main__':
    main()
