#author: Jakob Syvertsen

"""
This is the UserModel class.
It is the main class for everything related to the User directly, such as uploading and downloading calendars.
The UserModel class is also responsible for checking if a User has an account. 
"""
from DatabaseService import DatabaseService
from CalendarModel import CalendarModel
import EventModel
import AccountHandler

class UserModel:
    def __init__(self, userID, calendar): #Declaring the class
        self.userID = userID
        self.calendar = calendar

    def getID(self, user_ID): #gets the User ID of this User 
        # retrieve the user from the db
        # returns None if unavailable
        dbs = DatabaseService(self)

    def uploadCalendar(self, connection): #uploads a calendar file to the program 
        #not sure how connection is going to work for this, maybe have it in the declariation for the class?
        dbs = DatabaseService(self.calendar, connection)
        dbs.saveCalendar()

    def downloadCalendar(self, connection, calName): #downloads a calendar file from the program
        #also is this downloading from the database or from the website itself?
        dbs = DatabaseService(self.calendar, connection)
        if (dbs.getCalendar == null):
            cName = calName
            calModel = EventModel(self.calendar, cName)
            calModel.generateICSFile()
        else:
            cal = dbs.getCalendar(self.calendar)
        #ask the user what they would like to call the calendar (front end?)
        
    #not sure how to get the user the ability to view all    
    
    ############
    ## Should the user also access the delete/remove calendar functions from here?
    ############