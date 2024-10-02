import datetime

def current_utc_time():
    return datetime.datetime.now(datetime.timezone.utc)
