from datetime import datetime as dt



def Time(hour, minute, second, year=2023, month=1, day=1):
    return dt(year, month, day, hour, minute, second)
