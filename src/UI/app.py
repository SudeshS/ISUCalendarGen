# Author: Xavier Arriaga, Gordon (Tre) Blankenship
from CalendarModel import *
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import LoginManager
from accountHandler import AccountHandler as User
import os
import sys
from os.path import join, dirname, realpath
from flask_sqlalchemy import SQLAlchemy
from icalendar import Calendar, Event
sys.path.append("..")
# from static import uploads

##from iCalendar import Calendar, Event
#from wtforms import Form, BooleanField, StringField, PasswordField, validators
# ^ for validation if we have time for it, but this requires pip install Flask Flask-WTF

# This is the url that our server runs on
# host_URL =

#### NOTE: might have to rename to app.py for it to run properly ####
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cc30d0a491daf6a4ba282e9ea5f9dcfc994cb4b86d66f531'
login_manager = LoginManager()
login_manager.init_app(app)

# Messages is just a name, I was gonna switch it to classes
# but I couldn't get it to work for the time being, so keep it for now
# unless you know how to fix it
messages = [
    {'Summary': 'asdf', 'StartDate': '11/12/2022', 'StartTime': '11:00AM', 'Duration': '1H00M', 'UNTIL': '12/12/2022', 'BYDAY': 'FR', 'Description': 'ewofn132n', 'Location': '12r3'}, {
        'Summary': 'asdfg', 'StartDate': '09/12/2022', 'StartTime': '12:00PM', 'Duration': '1H15M', 'UNTIL': '12/15/2022', 'BYDAY': 'MO', 'Description': '21on241', 'Location': '12241'}
]


# debug mode toggle comment
app.config["DEBUG"] = True

# Upload folder
# this is where things will be stored locally until they can
# be integrated into the database
UPLOAD_FOLDER = app.static_folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER+'\\uploads\\'

# Login (on connection)
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']
        user1 = User(uname, pword)
        if not user1.login():
            error = 'Invalid Credentials. Please try again or create a new Account!'
        else:
            return redirect(url_for('home'))
    
    return render_template('login.html', error=error)

@app.route('/create_account/', methods=['GET', 'POST'])
def create_account():
    error = None

    if request.method == 'POST':
        uname = request.form['username']
        pword1 = request.form['password1']
        pword2 = request.form['password2']
        if pword1 != pword2:
            error = 'Please make sure the passwords match.'
        else:
            # **************SAVE TO DATABASE THE NEW USER HERE**********************
            
            return redirect(url_for('home'))

    return render_template('createAccount.html', error=error)

@app.route('/home/')
def home():
    return render_template('home.html')

# Upload page rendering
@app.route('/upload/')
def upload():
    # Set the upload HTML template '\templates\upload.html'
    return render_template('upload.html')

# Uploading files
@app.route('/upload/', methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        # save the file
    return redirect(url_for('upload'))

# Create page rendering
@app.route('/create/')
def index():
    return render_template('index.html', messages=messages)
    # these template files are key to this working

# Create handles the GET-ing of information from the form


@app.route('/calendar-preview/event/', methods=('GET', 'POST'))
def create():
    #event = Event()

    if request.method == 'POST':
        summary = request.form['Summary']
        startDate = request.form['StartDate']  # start date
        StartTime = request.form['StartTime']  # start time
        Duration = request.form['Duration']
        UNTIL = request.form['UNTIL']
        BYDAY = request.form['BYDAY']
        Description = request.form['Description']
        Location = request.form['Location']

        if not summary:
            flash('Class Name is required!')
        elif not startDate:
            flash('Start Date is required!')
        elif not StartTime:
            flash('Start Time is required')
        elif not Duration:
            flash('Duration is required')
        elif not UNTIL:
            flash('UNTIL is required')
        elif not BYDAY:
            flash('BYDAY is required')
        elif not Description:
            flash('Description is required')
        elif not Location:
            flash('Location is required')
        else:
            messages.append({'Summary': summary, 'StartDate': startDate, 'StartTime':StartTime, 'Duration': Duration,
                            'UNTIL': UNTIL, 'BYDAY': BYDAY, 'Description': Description, 'Location': Location})

            # change 0 index?
            event = CalendarModel.addEvents(list(messages))
            # cal.add_component(add_event)
            new_line = '\n'
            v_cal = 'END:VCALENDAR'

            with open('static/uploads/test_calendar.ics') as f:
                for line in f:
                    pass
                last_line = line

            if last_line == v_cal:
                with open('static/uploads/test_calendar.ics', "r+", encoding="utf-8") as file:

                    file.seek(0, os.SEEK_END)

                    pos = file.tell() - 1

                    while pos > 0 and file.read(1) != "\n":
                        pos -= 1
                        file.seek(pos, os.SEEK_SET)

                    if pos > 0:
                        file.seek(pos, os.SEEK_SET)
                        file.truncate()

            with open('static/uploads/test_calendar.ics') as f:
                for line in f:
                    pass
                last_line = line

            with open('static/uploads/test_calendar.ics', 'ab') as file:
                file.write(new_line.encode('utf-8'))
                file.write(event.to_ical())
                if last_line != v_cal:
                    file.write(v_cal.encode('utf-8'))

            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/calendar-preview/edit-event/', methods=('GET', 'POST'))
def edit():
    if request.method == 'POST':
        eventNum = request.form['EventNum']
        summary = request.form['Summary']
        startDate = request.form['StartDate']  # start date
        StartTime = request.form['StartTime']  # start time
        Duration = request.form['Duration']
        UNTIL = request.form['UNTIL']
        BYDAY = request.form['BYDAY']
        Description = request.form['Description']
        Location = request.form['Location']

        if not summary:
            flash('Class Name is required!')
        elif not startDate:
            flash('Start Date is required!')
        elif not StartTime:
            flash('Start Time is required')
        elif not Duration:
            flash('Duration is required')
        elif not UNTIL:
            flash('UNTIL is required')
        elif not BYDAY:
            flash('BYDAY is required')
        elif (int(eventNum) >= len(messages)) or (int(eventNum) < 0):
            flash('This Event ID does not exist')
        else:
            messages[int(eventNum)] = ({'Summary': summary, 'StartDate': startDate, 'StartTime': StartTime, 'Duration': Duration,
                            'UNTIL': UNTIL, 'BYDAY': BYDAY, 'Description': Description, 'Location': Location})
            return redirect(url_for('index'))

    return render_template('edit.html', messages=messages)


@app.route('/calendar-preview/remove-event/', methods=('GET', 'POST'))
def remove():
    if request.method == 'POST':
        # how do we get specific calendar/filename?
        filename = 'static/uploads/test_calendar.ics'
        eventNum = int(request.form['EventNum'])
        if (int(eventNum) >= len(messages)) or (int(eventNum) < 0):
            flash('This Event ID does not exist')
        else:
            CalendarModel.removeEvents(
                filename, list(messages[eventNum].values()))
            messages.pop(eventNum)
            return redirect(url_for('index'))

    return render_template('remove.html', messages=messages)


# Location should be kept not required alongside some others likely (description?)
if (__name__ == '__main__'):
    app.run(port=5000)
