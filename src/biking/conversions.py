import re

from datetime import date


def feet2miles(num):
    return float(num) / 5280


def meters2feet(num):
    return float(num) * 3.28084


def meters2miles(num):
    return float(num) / 1609.34


def mps2mph(num):
    return float(num) * 2.23694


def ymd2date(ymd):
    dt = None

    m = re.match(r"(\d\d\d\d)-(\d\d)-(\d\d)", ymd)
    if m:
        yyyy = m.group(1)
        mm = m.group(2)
        dd = m.group(3)
        dt = date(int(yyyy), int(mm), int(dd))

    return dt
