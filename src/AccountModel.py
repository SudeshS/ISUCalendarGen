#Author: Jakob Syvertsen

"""
This is the AccountModel class, which extends the User class.
It is the main class for dealing with User accounts.
In particular, it handles viewing saved calendars and editing saved calendars.
"""
class AccountModel:
    def __init__(self, username, password): #Declaring the class
        self.username = username
        self.password = password

    def viewAllSavedCalendars(): #shows the User all currently saved calendars
        pass

    def editSavedCalendar(): #allows the User to edit a saved calendar
        pass
