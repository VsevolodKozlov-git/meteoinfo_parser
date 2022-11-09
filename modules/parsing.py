# Мои модули
from modules.datetime_tools import get_date_str, get_unix_time
from modules.errors_and_types import DateDoesNotExist, TemperatureData
from modules.config import Config
# Внешние
from requests import post
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from time import sleep
from typing import List




def get_bs_for_date(dt: datetime) -> BeautifulSoup:
    unix_time = get_unix_time(dt)
    params = {'lang': 'ru-RU', 'id_city': 1659, 'dt': unix_time, 'had_db': 1, 'dop': 0}
    url = 'https://meteoinfo.ru/hmc-output/observ/obs_arch.php'
    response = post(url, params=params)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')


def parse_temperature(bs: BeautifulSoup) -> float:
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
        cur_dt += one_hour_delta
        print(f'Собраны данные для даты {date_str}. Засыпаю на {Config.sleep_time} секунды')
        sleep(Config.sleep_time)
    return data