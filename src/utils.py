import time


def read_api_version():
    with open('VERSION') as f:
        return f.read()


def iso_to_unix(iso_time):
    try:
        unix_timestamp = time.mktime(time.strptime(iso_time, "%Y-%m-%dT%H:%M:%S"))
        return int(unix_timestamp)
    except ValueError:
        raise ValueError("Invalid ISO time format")

