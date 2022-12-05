from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv


app = Flask(__name__)

# debug mode toggle comment
app.config["DEBUG"] = True
messages = []

# Database config, loads environment variables from .env file (don't put that file in github)
load_dotenv()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)


class Calendar(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  filename = db.Column(db.Text)
  file_data = db.Column(db.Text)

  def __init__(self, filename, file_data):
    self.filename = filename
    self.file_data = file_data

with app.app_context():
    db.create_all()

# Upload folder
# this is where things will be stored locally until they can
# be integrated into the database
UPLOAD_FOLDER = app.static_folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER+'\\uploads\\'


@app.route('/')
def index():
    return render_template('index.html', messages=messages)


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


@app.route('/upload/')
def upload():
    # Set the upload HTML template '\templates\index.html'
    return render_template('upload.html')


@app.route('/upload/', methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    if filename != '':
        #file_data = f"{uploaded_file.read()}"
        file_data = f"{uploaded_file.read().decode('utf-8')}"
        calendar = Calendar(filename, file_data)
        db.session.add(calendar)
        db.session.commit()

    return redirect(url_for('upload'))


if (__name__ == '__main__'):
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)