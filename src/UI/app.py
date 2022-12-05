# Author: Xavier Arriaga, Gordon (Tre) Blankenship
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import LoginManager
from accountHandler import AccountHandler as User
import os
from os.path import join, dirname, realpath

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
    # these files are key to this working

# Create handles the GET-ing of information from the form
@app.route('/class_preview/class/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        summary = request.form['Summary']
        DTStart = request.form['DTSTART']  # start date
        StartTime = request.form['StartTime']  # start time
        Duration = request.form['Duration']
        UNTIL = request.form['UNTIL']
        BYDAY = request.form['BYDAY']
        Description = request.form['Description']
        Location = request.form['Location']
        # DTStamp will be down on backend, will be time the event is created

        if not summary:
            flash('Class Name is required!')
        elif not DTStart:
            flash('Start Date is required!')
        elif not StartTime:
            flash('Start Time is required')
        elif not Duration:
            flash('Duration is required')
        elif not UNTIL:
            flash('UNTIL is required')
        elif not BYDAY:
            flash('BYDAY is required')
        else:
            messages.append({'Summary': summary, 'DTSTART': DTStart, 'Duration': Duration,
                            'UNTIL': UNTIL, 'BYDAY': BYDAY, 'Description': Description, 'Location': Location})
            return redirect(url_for('index'))

    return render_template('create.html')

# Location should be kept not required alongside some others likely (description?)
if (__name__ == '__main__'):
    app.run(port=5000)
