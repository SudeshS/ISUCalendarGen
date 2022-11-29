# Author: Xavier Arriaga
"""
This is the CalendarModel Class, aka Calendar.
It is the main class for creating, updating, and removing events.
It also deals with generating the ICSFile and generating a preview
"""

from CalendarPreview import CalendarPreview
from eventModel import EventModel
from calendar import month
from icalendar import Calendar, Event
from datetime import datetime, time


from CalendarPreview import CalendarPreview
from eventModel import EventModel
from calendar import month
from icalendar import Calendar, Event
from datetime import datetime, time


class CalendarModel:
    def __init__(self, calendarID, calendarName):  # Declaring the class
        self.calendarID = calendarID
        self.calendarName = calendarName

    # checks if the calendar is formated correctly
    def checkCalendarFormat(event_list):
        # if calendar generation is successful, returns true
        # else returns false
        try:
            CalendarModel.generateICSFile(event_list)
        except:
            return False

        return True

    # adds an event to passed in cal parameter
    def addEvents(self, cal):
        event = Event()

        # --- how does user know the UID? (Unique identifier within calendar)
        uid = input("UID: ")
        event.add('uid', uid)

        duration = input("Duration of class (ex. 1H15M): ")
        duration = time(hour=int(duration[0], minute=int(duration[2:3])))
        event.add('duration', duration)

        desc = input("Description: ")
        event.add('description', desc)

        # ---do we need desc and summary?
        summary = input("Summary: ")
        event.add('summary', summary)

        location = input("Location: ")
        event.add('location', location)

        start_date = input(
            "Start Date (ex. 01/17/2022): ")

        start_time = input(
            "Start Time (ex. 03:15PM, must include AM or PM): ")

        try:
            # PM
            if start_time[5] == 'P':
                if start_time[0:2] == '12':  # 12PM
                    start_time = str(start_time[0:2]) + str(start_time[3:5])
                else:                       # Any PM time other than 12PM
                    start_hour = int(start_time[0:2]) + 12
                    start_time = str(start_hour) + str(start_time[3:5])
            # AM
            elif start_time[5] == 'A':
                if start_time[0:2] == '12':  # 12AM
                    start_hour = '00'
                    start_time = start_hour + str(start_time[3:5])
                else:                       # Any AM time other than 12AM
                    start_time = str(start_time[0:2]) + str(start_time[3:5])

            start = datetime(year=int(start_date[6:10]), month=int(start_date[0:2]), day=int(start_date[3:5]),
                             hour=int(start_time[0:2]), minute=int(start_time[2:4]))

        except:
            print("\nStart time format incorrect")

        event.add('dtstart', start)

        freq = input("Frequency (Daily/Weekly/Yearly): ")
        byday = input(
            "By day - MO/TU/WE/TH/FR\nex1. MO,WE,FR  |   ex2. TU,TH: ")
        until = input("Last day of event (ex. 12/16/2022): ")
        # freq/byDay/until, convert until with datetime
        rrule = {
            'freq': freq,
            'byday': byday,
            'until': datetime(year=int(until[6:10]), month=int(until[0:2]), day=int(until[3:5]))
        }
        event.add('rrule', rrule)

        # dtstamp: when ics file was created --- do we need this?
        dtStamp = input("Stamp?")
        event.add('uid', uid)

        cal.add_component(event)

    # updates an event chosen by the user (might need to add an argument for that)
    def updateEvent(self, cal, newName, newTime, newDesc):
        # call removeEvents then call add events with new events

        #newName = input("Enter event Name: ")
        #newTime = input("Enter time slot (like xx:xx to xx:xx): ")
        #newDesc = input("Enter a short description on your event: ")
        self.event = EventModel(
            newName, newTime, newDesc, self.getCalendarID())
        self.event.editEvent()

    # although it might not matter for right now, actual users might want to have the ability to only edit one piece of info

    # removes the event or events given (may have to limit it to one event per call)
    def removeEvents(self, cal, uid):
        new_cal = Calendar()

        # ---do we want to find calender by UID or name? If UID, how will user know UID
        # copies cal to new_cal without removed event
        for k in cal.subcomponents:
            add_flag = False
            id_flag = False
            event = Event()

            for v in k:
                if id_flag == False:
                    # if UID matches, all subcomponents are skipped
                    if k.get(v)[0:9] == '2232-3620':
                        add_flag = True
                        break
                id_flag = True
                event.add(v, k.get(v))

            if add_flag == False:
                new_cal.add_component(event)

    # generates the ICSFile to be exported/downloaded (may need to return or print a string)
    def generateICSFile(event_list):
        cal = Calendar()
        cal.add('prodid', '-//Calendar Event Generator//')
        cal.add('version', '2.0')

        for i in range(len(event_list)):
            event = Event()

            # temp variable used to store split line
            # uid
            temp = event_list[i].uid.split(":", 1)
            event.add('uid', temp[1])

            # summary
            temp = event_list[i].summary.split(":", 1)
            event.add('summary', temp[1])

            # location
            temp = event_list[i].location.split(":", 1)
            event.add('location', temp[1])

            # dtstart
            temp = event_list[i].start.split(":", 1)
            date = datetime(year=int(temp[1][0:4]), month=int(
                temp[1][4:6]), day=int(temp[1][6:8]), hour=int(temp[1][9:11]), minute=int(temp[1][11:13]))
            event.add('dtstart', date)

            # rrule
            rrule = event_list[i].rule.split(":", 1)
            rrule = rrule[1].split(";")
            freq = rrule[0].split("=")
            byday = rrule[1].split("=")

            days = []
            byday = byday[1].split(',')  # num of days are dynamic
            for x in range(len(byday[1])):
                days.append(byday[x])
            until = rrule[2].split("=")

            rrule_dict = {
                'freq': freq[1],
                'byday': days,
                'until': datetime(year=int(until[1][0:4]), month=int(until[1][4:6]), day=int(until[1][6:8]))
            }
            event.add('rrule', rrule_dict)

            # dtend
            temp = event_list[i].start.split(":", 1)
            ftemp = event_list[i].duration.split(":")
            hour_var = int(ftemp[1][2:3])   # event hour duration
            hour_var = hour_var + int(temp[1][9:11])

            dur_minute = int(ftemp[1][4:6])  # event minute duration
            start_minute = int(temp[1][11:13])  # event start minute
            dur_minute = dur_minute + start_minute

            # if minutes over 60, add an hour and subtract 60
            if (dur_minute) > 60:
                hour_var = hour_var + 1
                dur_minute = dur_minute - 60

            end_timedate = datetime(year=int(temp[1][0:4]), month=int(
                temp[1][4:6]), day=int(temp[1][6:8]), hour=hour_var, minute=dur_minute)   # pass to dtend
            event.add('dtend', end_timedate)

    def checkCalendarFormat(): #checks if the calendar is formated correctly
        #will read in a file to ensure that the calendar that will be
        #generated is correctly formated.
        return bool

    def addEvents(self, eName, eTime, eDesc): #will add an event and return nothing
        #eName = input("Enter event Name: ")
        #eTime = input("Enter time slot (like xx:xx to xx:xx): ")
        #eDesc = input("Enter a short description on your event: ")
        self.event = eventModel(eName, eTime, eDesc, self.getCalendarID())
        pass

    def updateEvent(self, newName, newTime, newDesc): #updates an event chosen by the user (might need to add an argument for that) 
        #newName = input("Enter event Name: ")
        #newTime = input("Enter time slot (like xx:xx to xx:xx): ")
        #newDesc = input("Enter a short description on your event: ")
        self.event = eventModel(newName, newTime, newDesc, self.getCalendarID())
        self.event.editEvent()
        pass
    #although it might not matter for right now, actual users might want to have the ability to only edit one piece of info

    def removeEvents(self, event): #removes the event or events given (may have to limit it to one event per call)
        pass

    def generateICSFile(): #generates the ICSFile to be exported/downloaded (may need to return or print a string)
        #should call the ics_generator.py file?
        pass

    # gives a preview of what the calendar will look like (will need to generate calendar preview)
    def generatePreview(self, user):
        self.preview = CalendarPreview(self.getCalendarID(), user)
        self.preview.display()
        pass

    # Getters
    def getCalendarID(self):
        return self.calendarID

    def getCalendarName(self):
        return self.calendarName

    # Setters
    def setCalendarID(self, calID):
        self.calendarID = calID
        pass

    def setCalendarName(self, calName):
        self.calendarName = calName
        pass
