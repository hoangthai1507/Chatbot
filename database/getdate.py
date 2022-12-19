from datetime import datetime
from datetime import date
from datetime import timedelta


def get_today():
    now = datetime.now()  # current date and time
    d = now.strftime("%Y-%m-%d")
    return d


def get_yesterday():
    today = date.today()
    yesterday = today - timedelta(days=1)
    return yesterday.strftime("%Y-%m-%d")



