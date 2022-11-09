# Мои
from main import get_and_save_data
from modules.config import Config
# Внешние
from unittest import TestCase
from datetime import datetime
import pandas as pd


class IntegrationTestCase(TestCase):
    def test__get_data(self):
        start_date = datetime(day=20, month=10, year=2022, hour=1)
        end_date = datetime(day=20, month=10, year=2022, hour=4)
        xlsx_name = 'tmp.xlsx'
        get_and_save_data(start_date, end_date, xlsx_name)

        xlsx_path = Config.xlsx_dir_path / xlsx_name
        if not xlsx_path.resolve().is_file():
            raise AssertionError(f'xlsx файл с температурой не был создан')

        table = pd.read_excel(xlsx_path)
        expected_temperatures = [6, 6, 5.7, 5.6]
        for i in range(4):
            expected = expected_temperatures[i]
            actual = table.iloc[i, 1]
            hour = i + 1
            self.assertAlmostEqual(expected, actual, places=2, msg=f'Ошибка в {hour} часу 20.10.22')



