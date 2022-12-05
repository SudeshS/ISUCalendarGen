# Class to login, logout, delete, and create system accounts
class AccountHandler:

    # ---- only isLoggedIn is a parameter in class diagram
    def __init__(self, uname, pword):
        self.username = uname
        self.password = pword
        self.is_authenticated = False
        self.is_active = True
        self.is_anonymous = False

    def createAccount(self, uname, pword):
        self.username = uname
        self.password = pword

    # boolean
    def login(self):
        # take username and password
        # check if in DB
        # if in DB, take to user's account in DB
        # else, login failed
        return True

    def logout():
        # 
        pass

    def deleteAccount():
        # self.username = input("Username: ")
        # self.password = input("Password: ")
        pass

    def get(self, id):
        # simple typecast to retrieve
        # a str version of the userID
        uID = str(self.userID)
        return uID
    
    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password