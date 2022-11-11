from datetime import datetime, timedelta


def get_str_from_datetime(dt: datetime) -> str:
    return dt.strftime('%d/%m/%y %H:00')


def get_unix_time(dt: datetime) -> int:
    epoch = datetime.utcfromtimestamp(0)
    return int((dt - epoch).total_seconds())


def get_datetime_from_str(date_str: str) -> datetime:
    return datetime.strptime(date_str, '%d.%m.%y %H')


def each_hour_iter(start_date, end_date):
    cur_date= start_date
    while cur_date <= end_date:
        yield cur_date
        cur_date += timedelta(hours=1)
