from datetime import datetime


def get_date_str(dt: datetime) -> str:
    return dt.strftime('%d/%m/%y %H:00')


def get_unix_time(dt: datetime) -> int:
    epoch = datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds())


def get_datetime_from_str(date_str: str) -> datetime:
    return datetime.strptime(date_str, '%d.%m.%y %H')