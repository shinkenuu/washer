from datetime import datetime


def datetime_to_json_datetime(value: datetime):
    return value.strftime('%Y-%m-%d %H:%M:%S')


def json_datetime_to_datetime(value: str):
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
