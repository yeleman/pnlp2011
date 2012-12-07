#!/usr/bin/env python
# encoding=utf-8
# maintainer: alou/fad

from datetime import date
from bolibana.models import MonthPeriod


def rate_cal(*args):
    try:
        return (args[0] * 100) / args[1]
    except:
        return 0


def current_period():
    """ Period of current date """
    return MonthPeriod.find_create_by_date(date.today())
