from flask_login import UserMixin
from baseTable import Base, engine
from sqlalchemy import Column, Integer, Text
from werkzeug.security import generate_password_hash, check_password_hash

# Class to login, logout, delete, and create system accounts
class AccountHandler(UserMixin, Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing':True}
    id = Column(Integer, primary_key = True)
    username = Column(Text)
    password = Column(Text)

    # ---- only isLoggedIn is a parameter in class diagram
    def __init__(self, uname, pword):
        self.username = uname
        self.password = pword

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

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

Base.metadata.create_all(engine)