#Author: Jakob Syvertsen

"""
This is the AccountModel class, which extends the User class.
It is the main class for dealing with User accounts.
In particular, it handles viewing saved calendars and editing saved calendars.
"""
from UserModel import UserModel
from DatabaseService import DatabaseService #These two may not be needed
from CalendarModel import CalendarModel     #if inherit works like i think it does for python

class AccountModel(UserModel): #inherits the UserModel class
    def __init__(self, username, password): #Declaring the class
        self.username = username
        self.password = password

    def viewAllSavedCalendars(self, connection): #shows the User all currently saved calendars
        #again, not sure how we'll get the connection data for this.
        dbs = DatabaseService(self.calendar, connection)
        #for i in 
        #still not done, will likely require an if loop to go through a collect all the calendars?
        pass

    def editSavedCalendar(self, connection): #allows the User to edit a saved calendar
        dbs = DatabaseService(self.calendar, connection)
        cal = dbs.getCalendar(self.calendar)
        
        pass
