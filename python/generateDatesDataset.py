#!/usr/bin/env python
from datetime import date, timedelta

weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
sdate = date(1970, 1, 1)     # start date
edate = date(2069, 12, 31)   # end date
delta = edate - sdate        # as timedelta

print("Date,Count,Week,Day")
for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    # print(day & ",1")
    print str(day) + ",1," + str(day.isocalendar()[1]) + "," + weekDays[(day.weekday())]