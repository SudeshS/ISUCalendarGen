# Class to login, logout, delete, and create system accounts
class AccountHandler:

    # ---- only isLoggedIn is a parameter in class diagram
    def __init__(self, uID):
        self.username = ""
        self.password = ""
        self.userID = uID
        self.is_authenticated = False
        self.is_active = True
        self.is_anonymous = False

    def createAccount(self, uname, pword):
        self.username = uname
        self.password = pword

    def login():
        # take username and password
        # check if in DB
        # if in DB, take to user's account in DB
        # else, login failed
        pass

    def logout():
        # 
        pass

    def deleteAccount():
        # self.username = input("Username: ")
        # self.password = input("Password: ")
        pass

    def get_id(self):
        # simple typecast to retrieve
        # a str version of the userID
        uID = str(self.userID)
        return uID