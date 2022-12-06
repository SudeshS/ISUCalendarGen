# Author: Xavier Arriaga, Kaleb Liang
"""
This is the CalendarModel Class, aka Calendar.
It is the main class for creating, updating, and removing events.
It also deals with generating the ICSFile and generating a preview
"""


from CalendarPreview import CalendarPreview
from EventModel import EventModel
from calendar import month
from icalendar import Calendar, Event
from datetime import datetime, time
import os


class CalendarModel:
    def __init__(self):
        pass

    # determines how to parse a variable
    def determine_var(temp):
        if temp[0].upper() == 'SUMMARY':
            return temp[0], temp[1]
        elif temp[0].upper() == 'DTSTART':
            var_name = temp[0]
            temp = temp[1].split(":")
            date = datetime(year=int(temp[1][0:4]), month=int(
                temp[1][4:6]), day=int(temp[1][6:8]), hour=int(temp[1][9:11]), minute=int(temp[1][11:13]))
            return var_name, date
        ####
        elif temp[0] == 'DURATION': # reading from imported cal
            time_var = time(hour=int(temp[1][2:3]), minute=int(temp[1][4:6]))
            return temp[0], time_var
        elif temp[0] == 'Duration': # reading from messages
            time_var = time(hour=int(temp[1][0]), minute=int(temp[1][2:4]))
            return temp[0], time_var
        elif temp[0].upper() == 'DURATION;VALUE=TIME':  # reading from addEvents
            if len(temp) == 2:
                time_var = time(hour=int(temp[1][1:2]), minute=int(temp[1][2:4]))
            else:
                time_var = time(hour=int(temp[1]), minute=int(temp[2]))
            return temp[0], time_var
        elif temp[0].upper() == 'RRULE':
            rrule = temp[1].split(";")
            freq = rrule[0].split("=")
            byday = rrule[1].split("=")

            if byday[0] == 'UNTIL':
                byday = rrule[2].split("=")

            days = []
            byday = byday[1].split(',')  # num of days are dynamic
            # if only one day
            if (len(byday) == 1):
                days.append(byday[0])
            # else more than one day
            else:
                for x in range(len(byday)):
                    days.append(byday[x])
            until = rrule[2].split("=")

            if until[0] == 'BYDAY':
                until = rrule[1].split("=")

            rrule_dict = {
                'freq': freq[1],    #change to weekly?
                'byday': days,
                'until': datetime(year=int(until[1][0:4]), month=int(until[1][4:6]), day=int(until[1][6:8]))
            }
            return temp[0], rrule_dict
        elif temp[0].upper() == 'DESCRIPTION':
            return temp[0], temp[1]
        elif temp[0].upper() == 'LOCATION':
            return temp[0], temp[1]
        else:
            pass
            

    # parses calendar
    def parse_cal(filename):
        event_list = []
        with open(filename, 'r') as file:
            summary, start, duration, rule, desc, location = "","","","","",""
            for line in file:
                line = line.strip()
                line = line.replace('\\n', '')
                if line.startswith("SUMMARY"):
                    summary = line
                elif line.startswith("DTSTART"):
                    start = line
                elif line.startswith("DURATION"):
                    duration = line
                elif line.startswith("RRULE"):
                    rule = line
                elif line.startswith("DESCRIPTION"):
                    desc = line
                elif line.startswith("LOCATION"):
                    location = line
                elif line.startswith("END:VEVENT"):
                    event_list.append(
                        EventModel(summary, location, start, duration, rule, desc))

        return event_list

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
    def addEvents(dict, filename):
        event = Event()
        # most recent dict either at [0] or [len(dict)-1]
        # dict = dict[len(dict)-1]

        # ---might need to change duration to xx:xx
        # summary
        temp = list(dict.items())[0]
        e_type, temp = CalendarModel.determine_var(temp)
        event.add(e_type, temp)

        # duration
        temp = list(dict.items())[3]
        e_type, dur = CalendarModel.determine_var(temp)
        event.add(e_type, dur)

        start_date = list(dict.values())[1]
        start_time = list(dict.values())[2]

        # AM/PM conversions
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

        days = []
        until = list(dict.values())[4]
        byday = list(dict.values())[5]
        byday = byday.split('/')  # num of days are dynamic
        # if only one day
        if (len(byday) == 1):
            days.append(byday[0])
        # else more than one day
        else:
            for x in range(len(byday)):
                days.append(byday[x])
        # freq/byDay/until, convert until with datetime
        rrule = {
            'freq': 'WEEKLY',
            'byday': days,
            'until': datetime(year=int(until[6:10]), month=int(until[0:2]), day=int(until[3:5]))
        }
        event.add('rrule', rrule)

        end_datetime = datetime(year=start.year, month=start.month, day=start.day, hour=dur.hour, minute=dur.minute)
        event.add('dtend', end_datetime)

        desc = list(dict.values())[6]
        event.add('description', desc)

        location = list(dict.values())[7]
        event.add('location', location)

        new_line = '\n'
        v_cal = 'END:VCALENDAR'

        with open(filename) as f:
            for line in f:
                pass
            last_line = line

        if last_line == v_cal:
            with open(filename, "r+", encoding="utf-8") as file:

                file.seek(0, os.SEEK_END)

                pos = file.tell() - 1

                while pos > 0 and file.read(1) != "\n":
                    pos -= 1
                    file.seek(pos, os.SEEK_SET)

                if pos > 0:
                    file.seek(pos, os.SEEK_SET)
                    file.truncate()

        with open(filename) as f:
            for line in f:
                pass
            last_line = line

        with open(filename, 'ab') as file:
            if last_line != '':
                file.write(new_line.encode('utf-8'))   
            file.write(event.to_ical())
            if last_line != v_cal:
                file.write(v_cal.encode('utf-8'))

        return event

    # updates an event chosen by the user (might need to add an argument for that)
    def updateEvent(new_event, old_event, filename):
        # call removeEvents then call add events with new events
        var = CalendarModel.removeEvents(filename, old_event)
        if var:
            CalendarModel.addEvents(new_event, filename)

        # although it might not matter for right now, actual users might want to have the ability to only edit one piece of info

    # removes the event or events given (may have to limit it to one event per call)
    def removeEvents(file, messages):
        new_cal = Calendar()
        new_cal.add('prodid', '-//Calendar Event Generator//')
        new_cal.add('version', '2.0')
        return_flag = False


        event_list = CalendarModel.parse_cal(file)
        cal = CalendarModel.generateICSFile(event_list)

        # copies cal to new_cal without removed event
        for k in cal.subcomponents:
            add_flag = False
            # parameter for the event name to be removed
            event = Event()
            counter = 0

            for v in k:
                if counter < 1:  # will not enter if statement if no issues after 2nd iteration
                    var = k.get(v)
                    var = var.replace('\n', '')
                    # if name matches, set add_flag to true and break loop
                    if var.lower() == messages[0].lower():
                        add_flag = True
                        return_flag = True
                        break
                counter += 1
                event.add(v, k.get(v))

            # add_flag determines if event is added
            if add_flag == False:
                new_cal.add_component(event)

        with open('UI/static/uploads/test_calendar.ics', 'wb') as file:
            file.write(new_cal.to_ical().strip())
        
        return return_flag

    # generates the ICSFile to be exported/downloaded (may need to return or print a string)
    def generateICSFile(event_list):
        cal = Calendar()
        cal.add('prodid', '-//Calendar Event Generator//')
        cal.add('version', '2.0')

        for i in range(len(event_list)):
            event = Event()

            # summary
            temp = event_list[i].summary.split(":", 1)
            e_type, temp = CalendarModel.determine_var(temp)
            event.add(e_type, temp)

            # duration
            temp = event_list[i].duration.split(":")
            e_type, time_var = CalendarModel.determine_var(temp)
            event.add(e_type, time_var)

            # dtstart
            temp = event_list[i].start.split(";", 1)
            e_type, start_var = CalendarModel.determine_var(temp)
            event.add(e_type, start_var)

            # rrule
            rrule = event_list[i].rule.split(":", 1)
            e_type, temp = CalendarModel.determine_var(rrule)
            event.add(e_type, temp)


            # dtend NEED THIS
            temp = event_list[i].start.split(":", 1)
            ftemp = event_list[i].duration.split(":")
            if len(ftemp) == 2:
                hour_var = int(ftemp[1][1])   # event hour duration
                hour_var = hour_var + int(temp[1][9:11])
                dur_minute = int(ftemp[1][2:4])  # event minute duration
            else:
                hour_var = int(ftemp[1][1])
                hour_var = hour_var + int(temp[1][9:11])
                dur_minute = int(ftemp[2])
            start_minute = int(temp[1][11:13])  # event start minute
            dur_minute = dur_minute + start_minute

            # if minutes over 60, add an hour and subtract 60
            if (dur_minute) > 60:
                hour_var = hour_var + 1
                dur_minute = dur_minute - 60

            end_timedate = datetime(year=int(temp[1][0:4]), month=int(
                temp[1][4:6]), day=int(temp[1][6:8]), hour=hour_var, minute=dur_minute)   # pass to dtend
            
            event.add('dtend', end_timedate)

            # description
            temp = event_list[i].desc.split(":", 1)
            e_type, temp = CalendarModel.determine_var(temp)
            # event.add('description', temp[1])
            event.add(e_type, temp)

            # location
            temp = event_list[i].location.split(":", 1)
            e_type, temp = CalendarModel.determine_var(temp)
            # event.add('location', temp[1])
            event.add(e_type, temp)

            cal.add_component(event)

            # CalendarModel.setCalendarID =

        # do we write a file here or save file?
        # with open('data/output_isu_cal.ics', 'wb') as file:
        #     file.write(cal.to_ical())

        return cal

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
