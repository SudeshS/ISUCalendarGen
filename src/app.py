from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from accountHandler import AccountHandler as User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'cc30d0a491daf6a4ba282e9ea5f9dcfc994cb4b86d66f531'
app.config["DEBUG"] = True

login_manager = LoginManager()
login_manager.init_app(app)

messages = []

# Upload folder
UPLOAD_FOLDER = app.static_folder
app.config['UPLOAD_FOLDER'] = f"{UPLOAD_FOLDER}/uploads" # For macos/linux
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER+'\\uploads\\'

# Database config, loads environment variables from .env file (don't put that file in github)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    calendars = db.relationship('Calendar', backref='user')
    
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Calendar(db.Model):
  cal_id = db.Column(db.Integer, primary_key=True)
  filename = db.Column(db.Text)
  file_data = db.Column(db.Text)
  user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))

  def __init__(self, filename, file_data, user_id):
    self.filename = filename
    self.file_data = file_data
    self.user_id = user_id


with app.app_context():
    db.drop_all()
    db.session.commit()
    db.create_all()


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


@app.route('/upload/')
def upload():
    # Set the upload HTML template '\templates\index.html'
    return render_template('upload.html')


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

    return redirect(url_for('upload'))


# Create page rendering
@app.route('/create/')
def index():
    return render_template('index.html', messages=messages)
    # these files are key to this working


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


if (__name__ == '__main__'):
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)