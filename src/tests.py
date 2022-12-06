# testing file for all class and files used.
import pytest
import AccountHandler, AccountModel
import CalendarModel, CalendarPreview
import DatabaseConnection, DatabaseService
import EventModel, ics_generator
import server, UserModel

# accountHandler tests
def accountHandlerTest():
    
    user = AccountHandler.AccountHandler('admin', 'password')

    # login check
    assert AccountHandler.login('admin', 'password') == True
    assert AccountHandler.login('fake', 'account') == False
    
    # getUsername/Password checks
    assert user.getUsername() == 'admin'
    assert user.getPassword() == 'password'


# AccountModel tests

# CalendarModel tests

# CalendarPreview tests

# DatabaseConnection tests

# DatabaseService tests

# eventModel tests

# ics_generator tests

# server tests

# UserModel tests