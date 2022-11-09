from dataclasses import dataclass
from datetime import datetime


class DateDoesNotExist(Exception):
    """Ошибка появляющаяся если нет страницы на такой запрос"""


@dataclass(frozen=True)
class TemperatureData:
    temperature: float
    date: datetime
