#author: Jakob Syvertsen

"""
This is the UserModel class.
It is the main class for everything related to the User directly, such as uploading and downloading calendars.
The UserModel class is also responsible for checking if a User has an account. 
"""
class UserModel:
    def __init__(self, userID, isGuest): #Declaring the class
        self.userID = userID
        self.isGuest = isGuest

    def getID(): #gets the User ID of this User
        pass

    def isGuest(): #returns whether or not the current User is a guest (doesn't have an account)
        pass

    def uploadCalendar(): #uploads a calendar file to the program
        pass

    def downloadCalendar(): #downloads a calendar file from the program
        pass
    