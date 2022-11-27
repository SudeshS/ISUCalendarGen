# author: Kaleb Liang
# EventModel class contains all the data and methods of an event
from calendar import month
from icalendar import Calendar, Event
from datetime import datetime, time

class EventModel:
    def __init__(self, uid, summary, location, start, duration, rule, dtStamp, desc):
        self.uid = uid
        self.summary = summary
        self.location = location
        self.start = start
        self.duration = duration
        self.rule = rule
        self.dtStamp = dtStamp
        self.desc = desc

    # parses calendar --- should this go here?
    def parse_cal(filename):
        event_list = []
        with open(filename, 'r') as file:
            counter = 0
            # assume all imported ics files are of similar structure, only # of events change
            while True:
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

                    event_list.append(
                        EventModel(uid, summary, location, start, duration, rule, dtStamp, desc))

                if line == "":
                    counter = counter + 1
                    if counter > 3:
                        break

                
        return event_list

    # edit calendar events --- what about calendarModel methods?
    def editEvent(cal):
        # summary input box
        input1 = input()
        cal.update('summary', input1)

        #location
        #startTime/endTime (duration)
        #rule (freq/until/byDay)
        #description

    # getter
    def getCalendar(cal):
        return cal

    # merges events
    def mergeEvents():
        pass
 