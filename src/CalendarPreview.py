#Author: Xavier Arriaga
"""
Calendar Preview aggregates CalendarModel, it provide the means of downloading
the ics file/calendar/calendar in general, and allows a bit of post editing from
the preview itself in the form of removing objects
This should be created when generatePreview is called in the CalendarModel class
"""

class CalendarPreview:
    def __init__(cal, calendarID, user):
        cal.calendarID = calendarID
        cal.user = user

    #Display's the calendar in a somewhat readable way as a preview 
    def display(): 
        pass

    #removes an event from the preview rather than through the CalendarModel class (will need arguments?)
    def removeEvent(): 
        pass

    #prints the calendar from the preview so the user can download it in whichever way we offer it
    def print(): 
        pass

    #similar to print() this will just be an image of the calendar, probably nothing too complex
    def exportImage(): 
        pass

    #will remove the calendar generated through the ics file or that's been imported from the database
    def removeImportedCalendar(): 
        pass

    #Getters
    def getCalendarID(cal):
        return cal.calendarID

    def getUser(cal):
        return cal.user

    #Setters
    def setCalendarID(cal, calID):
        cal.calendarID = calID
        pass

    def setUser(cal, calUser):
        cal.User = calUser