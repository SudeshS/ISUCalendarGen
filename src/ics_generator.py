# authors: Sudesh Sahu, Kaleb Liang

from calendar import month
from icalendar import Calendar, Event
from datetime import datetime, time
import pytz
import uuid


class Events:
    def __init__(self, uid, summary, location, start, duration, rule, dtStamp, desc):
        self.uid = uid
        self.summary = summary
        self.location = location
        self.start = start
        self.duration = duration
        self.rule = rule
        self.dtStamp = dtStamp
        self.desc = desc
# test test


def parse_cal(filename):
    event_list = []
    with open(filename, 'r') as file:
        # assume all imported ics files are of similar structure, only # of events change
        while True:
            line = file.readline()
            # do we need first portion of calendar? (everything above VEVENT)
            if line == "END:VTIMEZONE\n":
                line = file.readline()
                line = file.readline()
            if line == "BEGIN:VEVENT\n":
                uid = file.readline()
                summary = file.readline()
                location = file.readline()
                start = file.readline()
                duration = file.readline()
                rule = file.readline()
                dtStamp = file.readline()
                desc = file.readline()
                # file.readline()
                event_list.append(
                    Events(uid, summary, location, start, duration, rule, dtStamp, desc))
            if line == "":
                break
    return event_list

    #     f_cal = Calendar.from_ical(file.read())
    # for component in f_cal.walk():
    #     if component.name == "VEVENT":
    #         print(component.get('summary'))
    #         print(component.get('dtstart').dt)
    #         print(component.get('dtend').dt)
    #         print(component.get('dtstamp').dt)


def create_cal(event_list):
    # ---used for testing---
    # cal1 = Calendar()
    # cal1.add('prodid', '-//Calendar Event Generator//')
    # cal1.add('version', '2.0')

    cal = Calendar()
    cal.add('prodid', '-//Calendar Event Generator//')
    cal.add('version', '2.0')

    for i in range(len(event_list)):
        event = Event()

        # temp variable used to store split line
        # uid
        temp = event_list[i].uid.split(":", 1)
        event.add('uid', temp[1])

        temp = event_list[i].summary.split(":", 1)
        event.add('summary', temp[1])

        temp = event_list[i].location.split(":", 1)
        event.add('location', temp[1])

        temp = event_list[i].start.split(":", 1)  # colon used to be semicolon
        date = datetime(year=int(temp[1][0:4]), month=int(
            temp[1][4:6]), day=int(temp[1][6:8]), hour=int(temp[1][9:11]), minute=int(temp[1][11:13]))
        event.add('dtstart', date)

        temp = event_list[i].duration.split(":")
        time_var = time(hour=int(temp[1][2:3]), minute=int(temp[1][4:6]))
        event.add('duration', time_var)

        rrule = event_list[i].rule.split(":", 1)
        rrule = rrule[1].split(";")
        freq = rrule[0].split("=")
        byday = rrule[1].split("=")

        days = []
        byday = byday[1].split(',')  # num of days are dynamic
        # if only one class
        if (len(byday) == 1):
            days.append(byday[0])
        # else more than one class
        else:
            for x in range(len(byday)):
                days.append(byday[x])
        until = rrule[2].split("=")

        rrule_dict = {
            'freq': freq[1],
            'byday': days,
            'until': datetime(year=int(until[1][0:4]), month=int(until[1][4:6]), day=int(until[1][6:8]))
        }
        event.add('rrule', rrule_dict)

        temp = event_list[i].dtStamp.split(":", 1)
        date = datetime(year=int(temp[1][0:4]), month=int(
            temp[1][4:6]), day=int(temp[1][6:8]), hour=int(temp[1][9:11]), minute=int(temp[1][11:13]), second=int(temp[1][13:]))
        event.add('dtstamp', date)

        event.add('description', event_list[i].desc.split(":", 1))
        cal.add_component(event)

    # with open('data/output_isu_cal.ics', 'wb') as file:
    #     file.write(cal1.to_ical())


def main():


<< << << << < Temporary merge branch 1
# CHANGE PATH FOR FINAL VERSION
f_path = 'data/input_isu_cal_i.ics'
== == == == =
# CHANGE PATH IF NECESSARY, TESTED ON MAC
f_path = 'ISUCalendarGen-1\src\data\input_isu_cal.ics'
>>>>>>>> > Temporary merge branch 2
event_list = parse_cal(f_path)
create_cal(event_list)


if __name__ == '__main__':
    main()
