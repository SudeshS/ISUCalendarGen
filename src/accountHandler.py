from flask_login import UserMixin, login_user, logout_user
from baseTable import Base, engine, db_session
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
        self.set_password(pword)

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def createAccount(uname, pword):
        existing_user = AccountHandler.query.filter_by(username=uname).first()
        if existing_user is None:
                user = AccountHandler(uname, pword)
                db_session.add(user)
                db_session.commit()
                login_user(user)
                return True
        return False

    # boolean
    @staticmethod
    def login(uname, pword):
        # take username and password
        # check if in DB
        # if in DB, take to user's account in DB
        # else, login failed
        user = AccountHandler.query.filter_by(username=uname).first()
        if user and user.check_password(pword):
            login_user(user)
            return True
        return False

    @staticmethod
    def logout():
        logout_user()

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