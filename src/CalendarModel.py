# Author: Xavier Arriaga
"""
This is the CalendarModel Class, aka Calendar.
It is the main class for creating, updating, and removing events.
It also deals with generating the ICSFile and generating a preview
"""


class CalendarModel:
    def __init__(cal, calendarID, calendarName):  # Declaring the class
        cal.calendarID = calendarID
        cal.calendarName = calendarName

    def checkCalendarFormat():  # checks if the calendar is formated correctly
        return bool

    def addEvents():  # will add an event and return nothing
        pass

    def updateEvent():  # updates an event chosen by the user (might need to add an argument for that)
        pass

    def removeEvents():  # removes the event or events given (may have to limit it to one event per call and will need arguments)
        pass

    def generateICSFile():  # generates the ICSFile to be exported/downloaded (may need to return or print a string)
        pass

    def generatePreview():  # gives a preview of what the calendar will look like (will need to present an image or text based image of some kind)
        pass

    # Getters
    def getCalendarID(cal):
        return cal.calendarID

    def getCalendarName(cal):
        return cal.calendarName

    # Setters
    def setCalendarID(cal, calID):
        cal.calendarID = calID
        pass

    def setCalendarName(cal, calName):
        cal.calendarName = calName
        pass
