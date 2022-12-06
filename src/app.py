from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from CalendarModel import *
from accountHandler import AccountHandler as User


app = Flask(__name__)

# load environment variables from .env file
load_dotenv()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config["DEBUG"] = True

login_manager = LoginManager()
login_manager.init_app(app)

messages = []

# Upload folder
UPLOAD_FOLDER = app.static_folder
app.config['UPLOAD_FOLDER'] = f"{UPLOAD_FOLDER}/uploads" # For macos/linux
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER+'\\uploads\\'

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)


# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.Text, unique=True)
#     password = db.Column(db.Text)
#     calendars = db.relationship('Calendar', backref='user')
    
#     def __init__(self, username, password):
#         self.username = username
#         self.set_password(password)

#     def set_password(self, password):
#         self.password = generate_password_hash(password, method='sha256')

#     def check_password(self, password):
#         return check_password_hash(self.password, password)


# class Calendar(db.Model):
#   cal_id = db.Column(db.Integer, primary_key=True)
#   filename = db.Column(db.Text)
#   file_data = db.Column(db.Text)
#   user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#   def __init__(self, filename, file_data, user_id):
#     self.filename = filename
#     self.file_data = file_data
#     self.user_id = user_id


# with app.app_context():
#     db.drop_all()
#     db.session.commit()
#     db.create_all()


# Login (on connection)
@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('login.html'))


# @app.route('/', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))

#     error = None
#     if request.method == 'POST':
#         uname = request.form['username']
#         pword = request.form['password']
#         user = User.query.filter_by(username=uname).first()
#         if user and user.check_password(pword):
#             login_user(user)
#             return render_template('home.html', current_user=current_user)
#         else:
#             error = 'Invalid Credentials. Please try again or create a new account'
#             flash(error)
#             return redirect(url_for('login'))
    
#     return render_template('login.html')

@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    error = None
    if request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']
        user = User.query.filter_by(username=uname).first()
        login_success = User.login(uname, pword)
        if login_success:
            #login_user(user)
            return render_template('home.html', current_user=current_user)
        else:
            error = 'Invalid Credentials. Please try again or create a new account'
            flash(error)
            return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    #logout_user()
    User.logout()
    return redirect(url_for('login'))


# @app.route('/create_account/', methods=['GET', 'POST'])
# def create_account():
#     error = None
#     if request.method == 'POST':
#         uname = request.form['username']
#         pword1 = request.form['password1']
#         pword2 = request.form['password2']
#         if pword1 != pword2:
#             error = 'Please make sure the passwords match.'
#             flash(error)
#         else:
#             # **************SAVE TO DATABASE THE NEW USER HERE**********************
#             existing_user = User.query.filter_by(username=uname).first()
#             if existing_user is None:
#                 user = User(uname, pword1)
#                 db.session.add(user)
#                 db.session.commit()
#                 login_user(user)
#                 return render_template('home.html', current_user=current_user)
#             flash('Error: A user already exists with that username.')

#     return render_template('createAccount.html')

@app.route('/create_account/', methods=['GET', 'POST'])
def create_account():
    error = None
    if request.method == 'POST':
        uname = request.form['username']
        pword1 = request.form['password1']
        pword2 = request.form['password2']
        if pword1 != pword2:
            error = 'Please make sure the passwords match.'
            flash(error)
        else:
            # **************SAVE TO DATABASE THE NEW USER HERE**********************
            account_created = User.createAccount(uname, pword1)
            if account_created:
                return render_template('home.html', current_user=current_user)
            flash('Error: A user already exists with that username.')

    return render_template('createAccount.html')


@app.route('/home/')
def home():
    return render_template('home.html', current_user=current_user)


@app.route('/upload/')
def upload():
    # Set the upload HTML template '\templates\index.html'
    return render_template('upload.html', current_user=current_user)


@app.route('/upload/', methods=['POST'])
def uploadFiles():
    # get the uploaded file
    # uploaded_file = request.files['file']
    # filename = uploaded_file.filename
    # if filename != '':
    #     #file_data = f"{uploaded_file.read()}"
    #     file_data = f"{uploaded_file.read().decode('utf-8')}"
    #     calendar = Calendar(filename, file_data)
    #     db.session.add(calendar)
    #     db.session.commit()

    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        # save the file

    return render_template('upload.html', current_user=current_user)


# Create page rendering
@app.route('/create/')
def index():
    return render_template('index.html', messages=messages, current_user=current_user)
    # these files are key to this working


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
            #event = CalendarModel.addEvents(list(messages))
            return render_template('index.html', messages=messages, current_user=current_user)

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
            return render_template('index.html', messages=messages, current_user=current_user)

    return render_template('edit.html', messages=messages, current_user=current_user)


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
            return render_template('index.html', messages=messages, current_user=current_user)

    return render_template('remove.html', messages=messages, current_user=current_user)


if (__name__ == '__main__'):
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
