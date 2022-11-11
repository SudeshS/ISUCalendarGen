#Author: Xavier Arriaga
"""
This is the CalendarModel Class, aka Calendar.
It is the main class for creating, updating, and removing events.
It also deals with generating the ICSFile and generating a preview
"""
import eventModel
import CalendarPreview 

class CalendarModel:
    def __init__(self, calendarID, calendarName): #Declaring the class
        self.calendarID = calendarID
        self.calendarName = calendarName 

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

    def generatePreview(self, user): #gives a preview of what the calendar will look like (will need to generate calendar preview)
        self.preview = CalendarPreview(self.getCalendarID(), user)
        self.preview.display()
        pass

    #Getters
    def getCalendarID(self):
        return self.calendarID

    def getCalendarName(self):
        return self.calendarName

    #Setters
    def setCalendarID(self, calID):
        self.calendarID = calID
        pass

    def setCalendarName(self, calName):
        self.calendarName = calName
        pass
