from flask import Flask, render_template, request, url_for, flash, redirect, send_file
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from CalendarModel import *
from AccountHandler import AccountHandler as User


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


@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    error = None
    if request.method == 'POST':
        uname = request.form['username']
        pword = request.form['password']
        login_success = User.login(uname, pword)
        if login_success:
            return redirect(url_for('home'))
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
    result = db.session.execute("SELECT * FROM calendar")
    return render_template("home.html", data=result, current_user=current_user)


@app.route('/upload/')
def upload():
    # Set the upload HTML template '\templates\index.html'
    return render_template('upload.html', current_user=current_user)

#upload file to database
@app.route('/upload/', methods=['POST'])
def uploadFiles():
    uploadfile = request.files['file']
    if request.method == 'POST':
        if uploadfile.filename != '':
            filename=uploadfile.filename
            readfile = uploadfile.read()
            file_data = '{}'.format(readfile)
            cform = CalendarTable(filename, file_data, current_user.id)
            db.session.add(cform)
            db.session.commit()
    return redirect(url_for('home'))

#Preview list of calendars
#@app.route('/home', methods=['POST'])
#def display():
    #result = db.session.execute("SELECT * FROM calendar")
    #return render_template("home.html", data=result)

#Download calendar from database
@app.route("/calendarSave/<int:calendarid>")
def calendarSave(calendarid):
    filepath = os.path.dirname(__file__)
    rel_path = "exportedcalendar.ics"
    abs_file_path = os.path.join(filepath, rel_path)
    f = open(abs_file_path, 'w')
    saveCal = db.session.query(CalendarTable).filter(CalendarTable.id==calendarid)
    for saveFile in saveCal:
        saveFile.file_data = saveFile.file_data.strip('\'')
        saveFile.file_data = saveFile.file_data.replace('\\r\\n', '\n')
        saveFile.file_data = saveFile.file_data.replace('b\'', '')
        f.write(saveFile.file_data)
        f.close()
    return send_file('exportedcalendar.ics', mimetype='text/calendar', as_attachment=True)

#Delete calendar form database
@app.route("/calendarDelete/<int:calendarid>")
def calendarDelete(calendarid):
    strDB="delete from calendar where id="+str(calendarid)
    db.session.execute(strDB)
    db.session.commit()
    return redirect(url_for('home'))

#access calendar modification
#@app.route("/calendarModify/<int:calendarid>")
#def calendarModify(calendarid):
   # strModify="SELECT * FROM calendar where id="+str(calendarid)
    #calendar=db.session.execute(strModify)
   # return render_template("modifyCalendar.html",calendarinfo=calendar)


# Create page rendering
@app.route('/index/')
def index():
    return render_template('index.html', messages=messages, current_user=current_user)
    # these files are key to this working


@app.route('/preview/')
def preview():
    return render_template('preview.html', messages=messages, current_user=current_user)


@app.route("/create/<int:calendarid>", methods=('GET', 'POST'))
def create(calendarid):
    modifyCal = db.session.query(CalendarTable).filter(CalendarTable.id==calendarid).one()
    file_data = modifyCal.file_data
    local_file = open("localfile.ics", "w")
    file_data = file_data.strip('\'')
    file_data = file_data.replace('\\r\\n', '\n')
    file_data = file_data.replace('b\'', '')
    local_file.write(file_data)
    local_file.close()
    filename = 'localfile.ics'

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

            event = CalendarModel.addEvents(messages[-1], filename)
            
            with open(filename, "r+", encoding="utf-8") as file:
                file_content = file.read()
                modifyCal.file_data = file_content
                db.session.commit()

            return render_template('index.html', messages=messages, current_user=current_user, calendarid=calendarid)
        

    return render_template('create.html')


@app.route('/calendar-preview/edit-event/<int:calendarid>', methods=('GET', 'POST'))
def edit(calendarid):
    modifyCal = db.session.query(CalendarTable).filter(CalendarTable.id==calendarid).one()
    file_data = modifyCal.file_data
    local_file = open("localfile.ics", "w")
    file_data = file_data.strip('\'')
    file_data = file_data.replace('\\r\\n', '\n')
    file_data = file_data.replace('b\'', '')
    local_file.write(file_data)
    local_file.close()
    filename = 'localfile.ics'
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
            old_event = messages[int(eventNum)]
            messages[int(eventNum)] = ({'Summary': summary, 'StartDate': startDate, 'StartTime': StartTime, 'Duration': Duration,
                            'UNTIL': UNTIL, 'BYDAY': BYDAY, 'Description': Description, 'Location': Location})
            CalendarModel.updateEvent(
                messages[int(eventNum)], list(old_event.values()), filename) 
            return render_template('index.html', messages=messages, current_user=current_user, calendarid=calendarid)

    return render_template('edit.html', messages=messages, current_user=current_user)


@app.route('/calendar-preview/remove-event/<int:calendarid>', methods=('GET', 'POST'))
def remove(calendarid):
    if request.method == 'POST':
        # how do we get specific calendar/filename?
        modifyCal = db.session.query(CalendarTable).filter(CalendarTable.id==calendarid).one()
        file_data = modifyCal.file_data
        local_file = open("localfile.ics", "w")
        file_data = file_data.strip('\'')
        file_data = file_data.replace('\\r\\n', '\n')
        file_data = file_data.replace('b\'', '')
        local_file.write(file_data)
        local_file.close()
        filename = 'localfile.ics'
        eventNum = int(request.form['EventNum'])
        if (int(eventNum) >= len(messages)) or (int(eventNum) < 0):
            flash('This Event ID does not exist')
        else:
            CalendarModel.removeEvents(
                filename, list(messages[eventNum].values()))
            messages.pop(eventNum)
            return render_template('index.html', messages=messages, current_user=current_user, calendarid=calendarid)

    return render_template('remove.html', messages=messages, current_user=current_user, calendarid=calendarid)


if (__name__ == '__main__'):
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
