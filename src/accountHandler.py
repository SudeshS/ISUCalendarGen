# Class to login, logout, delete, and create system accounts
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import app
from app import db

class AccountHandler(UserMixin, db.Model):
    
    # __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    calendars = db.relationship('Calendar', backref='user')


    # ---- only isLoggedIn is a parameter in class diagram
    def __init__(self, uname, pword):
        self.username = uname
        self.set_password(pword)
        self.is_authenticated = False
        self.is_active = True
        self.is_anonymous = False
    
    def set_password(self, pword):
        self.password = generate_password_hash(pword, method='sha256')

    def check_password(self, pword):
        return check_password_hash(self.password, pword)
    
    def createAccount(self, uname, pword):
        self.username = uname
        self.password = pword

    # boolean
    def login(self):
        # take username and password
        # check if in DB
        # if in DB, take to user's account in DB
        # else, login failed
        if self.query.filter_by(username=self.username).first() and self.check_password(self.password):
            login_user(self)
            return True
        else:
            return False
        

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


with app.app_context():
    # db.drop_all()
    # db.session.commit()
    db.create_all()