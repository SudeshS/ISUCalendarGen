# Author: Xavier Arriaga, Gordon (Tre) Blankenship
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_login import LoginManager
from os.path import join, dirname, realpath
from flask_sqlalchemy import SQLAlchemy

#### NOTE: might have to rename to app.py for it to run properly ####
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cc30d0a491daf6a4ba282e9ea5f9dcfc994cb4b86d66f531'

# Messages is just a name, I was gonna switch it to classes
# but I couldn't get it to work for the time being, so keep it for now
# unless you know how to fix it
messages = [
]

# enable debugging mode
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:isu@localhost/CalendarDatabase'

db = SQLAlchemy(app)

# Upload folder
# this is where things will be stored locally until they can
# be integrated into the database
UPLOAD_FOLDER = app.static_folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER+'\\uploads\\'


class CForm(db.Model):
    __tablename__ = 'calendars'
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.Text)

    def __init__(self, file):
        self.file = file
# Root URL - What the user connects to


@app.route('/')
def index():
    # Set the upload HTML template '\templates\index.html'
    return render_template('upload.html')

# Uploading files


@app.route('/upload/', methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file = uploaded_file
        cform = CForm(file)
        db.session.add(cform)
        db.session.commit()
        #file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        # uploaded_file.save(file_path)
        # save the file
    return redirect(url_for('upload'))

# Create page rendering


@app.route('/create/')
def index():
    return render_template('index.html', messages=messages)
    # these files are key to this working

# Create handles the GET-ing of information from the form


@app.route('/create/class/', methods=('GET', 'POST'))
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


with app.app_context():
    db.create_all()

if (__name__ == '__main__'):
    app.run(port=5000)
