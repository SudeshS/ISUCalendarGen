# Class to login, logout, delete, and create system accounts
class AccountHandler:

    # ---- only isLoggedIn is a parameter in class diagram
    def __init__(self, uID):
        self.username = ""
        self.password = ""
        self.isLoggedIn = False

    def createAccount(self):
        self.username = input("Username: ")
        self.password = input("Password: ")

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
