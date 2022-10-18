from main import save_to_xlsx, TemperatureData
from datetime import datetime
from unittest import TestCase
import xlsxwriter


class XlsxSaverTestCase(TestCase):
    def get_date(self, date_str):
        return datetime.strptime(date_str, '%d.%m.%y %H')

    def test__save_data(self):
        dates = ['16.10.22 8',
                 '16.10.22 9',
                 '15.10.22 09']
        dates = [self.get_date(i) for i in dates]

        temperatures = [20, 0.4, 1.34]
        data = [TemperatureData(temp, date) for temp, date in zip(temperatures, dates)]
        save_to_xlsx(data, 'tmp')


    def test__package_write_data(self):
        workbook = xlsxwriter.Workbook('tmp.xlsx')
        worksheet = workbook.add_worksheet()
        # worksheet.write_datetime