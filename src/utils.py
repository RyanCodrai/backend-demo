from dateutil import parser


def read_api_version():
    with open('VERSION') as f:
        return f.read()


def iso_to_unix(iso_time):
    try:
        dt = parser.isoparse(iso_time)

        unix_timestamp = int(dt.timestamp())
        return unix_timestamp
    except ValueError:
        raise ValueError("Invalid ISO time format")

