# Мои
from main import get_and_save_data
from modules.config import Config
from modules.datetime_tools import get_str_from_datetime
# Внешние
from unittest import TestCase
from datetime import datetime, timedelta
import pandas as pd


class IntegrationTestCase(TestCase):

    def check_date(self, start_date, end_date, expected_temperatures):
        xlsx_name = 'tmp.xlsx'
        get_and_save_data(start_date, end_date, xlsx_name)

        xlsx_path = Config.xlsx_dir_path / xlsx_name
        if not xlsx_path.resolve().is_file():
            raise AssertionError(f'xlsx файл с температурой не был создан')

        table = pd.read_excel(xlsx_path)
        date = start_date
        for i, expected in enumerate(expected_temperatures):
            actual = table.iloc[i, 1]
            self.assertAlmostEqual(expected, actual, places=2,
                                   msg=f'Ошибка в дате {get_str_from_datetime(date)}')
            date += timedelta(hours=1)
    def test__nonempty_dates(self):
        start_date = datetime(day=20, month=10, year=2022, hour=2)
        end_date = datetime(day=20, month=10, year=2022, hour=3)
        expected_temperatures = [6, 5.7]
        self.check_date(start_date, end_date, expected_temperatures)

    def test_empty_dates(self):
        start_date = datetime(day=1, month=10, year=2022, hour=2)
        end_date = datetime(day=1, month=10, year=2022, hour=3)
        expected_temperatures = [12.4]
        self.check_date(start_date, end_date, expected_temperatures)




