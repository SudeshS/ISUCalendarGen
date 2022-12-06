# Author: Jakob Syvertsen

"""
This is the AccountModel class, which extends the User class.
It is the main class for dealing with User accounts.
In particular, it handles viewing saved calendars and editing saved calendars.
"""
from UserModel import UserModel
from DatabaseService import DatabaseService  # These two may not be needed
# if inherit works like i think it does for python
from EventModel import EventModel


class AccountModel(UserModel):  # inherits the UserModel class
    def __init__(self, username, password):  # Declaring the class
        self.username = username
        self.password = password

    # shows the User all currently saved calendars
    def viewAllSavedCalendars(self, connection):
        # again, not sure how we'll get the connection data for this.
        dbs = DatabaseService(self.calendar, connection)
        # for i in
        # still not done, will likely require an if loop to go through a collect all the calendars?
        pass

    # allows the User to edit a saved calendar
    def editSavedCalendar(self, connection):
        dbs = DatabaseService(self.calendar, connection)
        cal = dbs.getCalendar(self.calendar)

        pass
