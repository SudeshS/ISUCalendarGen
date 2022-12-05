import DatabaseConnection

class DatabaseService():
    def __init__(self, calendar, connection):
        self.calendar = calendar
        self.connection = connection
    

    def saveCalendar(self):
        pass

    
    def deleteCalendar(self):
        pass


    def removeFromDB(self):
        pass


    def getCalendar(self, calendar): #needs a check to see if the calendar is indeed there and if not send a null calendar?
        #also needs to return the calendar, so we'll likely need another attribute for a calendar object
        pass