import datetime
from datetime import time


def demand(t, annual_demand=50):  # zapotrzebowanie w MWh
    return annual_demand / (365 * 24)


def step_demand(t, dates, annual_demand=50):
    def is_workday(date):
        return date.weekday() in range(5)

    def is_day(date):
        return (date.time() <= time(19, 00)) and (date.time() >= time(8, 00))

    daily = annual_demand / (250 * 24)
    return [daily if is_workday(date) and is_day(date) else 0 for date in dates]

