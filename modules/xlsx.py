# Мои модули
from modules.errors_and_types import TemperatureData
from modules.config import Config
# Внешние модули
from typing import List
import xlsxwriter


def save_to_xlsx(data: List[TemperatureData], xlsx_name: str) -> None:
    xlsx_file_path = Config.xlsx_dir_path / xlsx_name
    workbook = xlsxwriter.Workbook(xlsx_file_path)
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