import re

from datetime import date


def feet2miles(num):
    return float(num) / 5280


def kj2kcal(num):
    return num * 0.239


def meters2feet(num):
    return float(num) * 3.28084


def meters2miles(num):
    return float(num) / 1609.34


def mps2mph(num):
    return float(num) * 2.23694


def period2days(period):
    days = 0

    if period == "last30":
        days = 30
    elif period == "last60":
        days = 60
    elif period == "last90":
        days = 90

    return days


def ymd2date(ymd):
    dt = None

    m = re.match(r"(\d\d\d\d)-(\d\d)-(\d\d)", ymd)
    if m:
        yyyy = m.group(1)
        mm = m.group(2)
        dd = m.group(3)
        dt = date(int(yyyy), int(mm), int(dd))

    return dt
