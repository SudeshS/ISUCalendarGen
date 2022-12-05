from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_login import LoginManager
import os
from os.path import join, dirname, realpath
from flask_sqlalchemy import SQLAlchemy
from icalendar import Calendar, Event
import psycopg2
# login_manager = LoginManager()
app = Flask(__name__)
# login_manager.init_app(app)

# enable debugging mode
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:isu@localhost/CalendarDatabase'
con = psycopg2.connect(database="CalendarDatabase", user="postgres", password="isu", host="localhost", port="5432")
cursor=con.cursor()

db=SQLAlchemy(app)

# Upload Folder
UPLOAD_FOLDER = app.static_folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER+'\\uploads\\'

class CForm(db.Model):
  __tablename__='calendars'
  id=db.Column(db.Integer,primary_key=True)
  file=db.Column(db.Text)
  filename=db.Column(db.Text)

  def __init__(self,file,filename):
    self.file=file
    self.filename=filename
# Root URL - What the user connects to
@app.route('/')
def index():
    # Set the upload HTML template '\templates\index.html'
    return render_template('upload.html')
# Uploading files
@app.route("/", methods=['POST', 'GET'])
def uploadFiles():
    # get the uploaded file
    uploadfile = request.files['file']
    if request.method == 'POST':
        if uploadfile.filename != '':
            filename=uploadfile.filename
            readfile = uploadfile.read()
            file = '{}'.format(readfile)
            cform = CForm(file,filename)
            db.session.add(cform)
            db.session.commit()

            

            #file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            # set the file path
            #uploaded_file.save(file_path)
            # save the file
        return redirect(url_for('index'))
@app.route('/display', methods=['POST'])
def display():
    result = db.session.execute("SELECT * FROM calendars")
    return render_template("display.html", data=result)
@app.route("/calendarSave/<int:calendarid>")
def calendarSave(calendarid):
    filepath = os.path.dirname(__file__)
    rel_path = "exportedcalendar.ics"
    abs_file_path = os.path.join(filepath, rel_path)
    f = open(abs_file_path, 'w')
    saveCal = db.session.query(CForm).filter(CForm.id==calendarid)
    for saveFile in saveCal:
        saveFile.file = saveFile.file.strip('\'')
        saveFile.file = saveFile.file.replace('\\r\\n', '\n')
        saveFile.file = saveFile.file.replace('b\'', '')
        f.write(saveFile.file)
        f.close()
    return send_file('exportedcalendar.ics', mimetype='text/calendar', as_attachment=True)

@app.route("/calendarDelete/<int:calendarid>")
def calendarDelete(calendarid):
    strDB="delete from calendars where id="+str(calendarid)
    db.session.execute(strDB)
    db.session.commit()
    return render_template("upload.html")

with app.app_context():
    db.create_all()

if (__name__ == '__main__'):
    app.run(port = 5000)