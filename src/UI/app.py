# Author: Xavier Arriaga, Gordon (Tre) Blankenship
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import LoginManager
import os
import sys
from os.path import join, dirname, realpath
from flask_sqlalchemy import SQLAlchemy
from icalendar import Calendar, Event
sys.path.append("..")
from CalendarModel import *
# from static import uploads

##from iCalendar import Calendar, Event
#from wtforms import Form, BooleanField, StringField, PasswordField, validators
# ^ for validation if we have time for it, but this requires pip install Flask Flask-WTF

# This is the url that our server runs on
# host_URL =

#### NOTE: might have to rename to app.py for it to run properly ####
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cc30d0a491daf6a4ba282e9ea5f9dcfc994cb4b86d66f531'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:isu@localhost/calendarform'

db = SQLAlchemy(app)

# Messages is just a name, I was gonna switch it to classes
# but I couldn't get it to work for the time being, so keep it for now
# unless you know how to fix it
messages = [
    
]


# debug mode toggle comment
app.config["DEBUG"] = True

# Upload folder
# this is where things will be stored locally until they can
# be integrated into the database
UPLOAD_FOLDER = app.static_folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER+'\\uploads\\'


class CForm(db.Model):
    # __tablename__='calendar'
    # id=db.Column(db.Integer,primary_key=True)
    # summary=db.Column(db.String())
    # DTStart=db.Column(db.String())
    # StartTime=db.Column(db.String())
    # Duration=db.Column(db.String())
    # UNTIL=db.Column(db.String())
    # BYDAY=db.Column(db.String())
    # Description=db.Column(db.Text)
    # Location=db.Column(db.Text)
    __tablename__ = 'calendars'
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.Text)

    def __init__(self, file):
        # self.summary=summary
        # self.DTStart=DTStart
        # self.StartTime=StartTime
        # self.Duration=Duration
        # self.UNTIL=UNTIL
        # self.BYDAY=BYDAY
        # self.Description=Description
        # self.Location=Location
        self.file = file


# Upload page rendering
@app.route('/upload/')
def upload():
    # Set the upload HTML template '\templates\index.html'
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


@app.route('/')
def index():
    return render_template('index.html', messages=messages)
    # these template files are key to this working

# Create handles the GET-ing of information from the form


@app.route('/class-preview/class/', methods=('GET', 'POST'))
def create():
    filename = 'static/uploads/test_calendar.ics'

    if request.method == 'POST':
        summary = request.form['Summary']
        StartDate = request.form['StartDate']  # start date
        StartTime = request.form['StartTime']  # start time
        Duration = request.form['Duration']
        UNTIL = request.form['UNTIL']
        BYDAY = request.form['BYDAY']
        Description = request.form['Description']
        Location = request.form['Location']

        if not summary:
            flash('Class Name is required!')
        elif not StartDate:
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
            messages.append({'Summary': summary, 'StartDate': StartDate, 'StartTime': StartTime, 'Duration': Duration,
                            'UNTIL': UNTIL, 'BYDAY': BYDAY, 'Description': Description, 'Location': Location})

            # change 0 index?
            event = CalendarModel.addEvents(messages[len(messages)-1], filename)

            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/class-preview/edit-class/', methods=('GET', 'POST'))
def edit():
    filename = 'static/uploads/test_calendar.ics'   # change
    if request.method == 'POST':
        eventNum = request.form['EventNum']
        summary = request.form['Summary']
        StartTime = request.form['StartTime']  # start date
        StartTime = request.form['StartTime']  # start time
        Duration = request.form['Duration']
        UNTIL = request.form['UNTIL']
        BYDAY = request.form['BYDAY']
        Description = request.form['Description']
        Location = request.form['Location']

        if not summary:
            flash('Class Name is required!')
        elif not StartTime:
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
            flash('The Event number does not exist')
        else:
            old_event = messages=[int(eventNum)]
            messages[int(eventNum)] = ({'Summary': summary, 'DTSTART': StartTime, 'StartTime': StartTime, 'Duration': Duration,
                                        'UNTIL': UNTIL, 'BYDAY': BYDAY, 'Description': Description, 'Location': Location})
            CalendarModel.updateEvent(list(messages[int(eventNum)]), list(old_event.values()), filename)
            return redirect(url_for('index'))

    return render_template('edit.html')


@app.route('/class-preview/remove-class/', methods=('GET', 'POST'))
def remove():
    if request.method == 'POST':
        # how do we get specific calendar/filename?
        filename = 'static/uploads/test_calendar.ics'
        eventNum = int(request.form['EventNum'])
        if (int(eventNum) >= len(messages)) or (int(eventNum) < 0):
            flash('The Event number does not exist')
            # doesnt let me remove 0
        else:
            CalendarModel.removeEvents(
                filename, list(messages[eventNum].values()))
            messages.pop(eventNum)
            return redirect(url_for('index'))

    return render_template('remove.html')


# Location should be kept not required alongside some others likely (description?)
if (__name__ == '__main__'):
    app.run(port=5000)
