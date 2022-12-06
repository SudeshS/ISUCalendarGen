# testing file for all class and files used.
import pytest
import accountHandler, AccountModel
import CalendarModel, CalendarPreview
import DatabaseConnection, DatabaseService
import eventModel, ics_generator
import server, UserModel

# accountHandler tests
def accountHandlerTest():
    
    user = accountHandler.AccountHandler('admin', 'password')

    # login check
    assert accountHandler.login('admin', 'password') == True
    assert accountHandler.login('fake', 'account') == False
    
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