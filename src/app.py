from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)

# debug mode toggle comment
app.config["DEBUG"] = True
messages = []

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)


class CForm(db.Model):
  __tablename__ = 'calendars'
  id = db.Column(db.Integer,primary_key=True)
  file = db.Column(db.Text)

  def __init__(self,file):
    self.file = file



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
    if uploaded_file.filename != '':
        file_path = os.path.join(
            app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        # save the file
    return redirect(url_for('upload'))


if (__name__ == '__main__'):
    app.run(port=5000)