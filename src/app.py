from flask import Flask, render_template, request, url_for, flash, redirect
from icalendar import Calendar, Event
from flask_sqlalchemy import SQLAlchemy

#### NOTE: might have to rename to app.py for it to run properly ####
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:isu@localhost/calendarform'

db=SQLAlchemy(app)

#Messages is just a name, I was gonna switch it to classes
# but I couldn't get it to work for the time being, so keep it for now
# unless you know how to fix it
messages = [
            ]

class CForm(db.Model):
    __tablename__='calendar'
    id=db.Column(db.Integer,primary_key=True)
    summary=db.Column(db.String())
    DTStart=db.Column(db.DateTime)
    DTEnd=db.Column(db.DateTime)
    Duration=db.Column(db.Time)
    UNTIL=db.Column(db.DateTime)
    BYDAY=db.Column(db.String())
    Description=db.Column(db.Text)
    Location=db.Column(db.Text)   

    def __init__(self,summary,DTStart,DTEnd,Duration,UNTIL,BYDAY,Description,Location):
        self.summary=summary
        self.DTStart=DTStart
        self.DTEnd=DTEnd
        self.Duration=Duration
        self.UNTIL=UNTIL
        self.BYDAY=BYDAY
        self.Description=Description
        self.Location=Location



@app.route('/')
def index():
    return render_template('index.html', messages=messages)

#Create handles the GET-ing of information from the form
@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        summary = request.form['Summary']
        DTStart = request.form['DTSTART']
        DTEnd = request.form['DTEND']
        Duration = request.form['Duration']
        UNTIL = request.form['UNTIL']
        BYDAY = request.form['BYDAY']
        Description = request.form['Description']
        Location = request.form['Location']
        # DTStamp will be down on backend, will be time the event is created

        cform=CForm(summary,DTStart,DTEnd,Duration,UNTIL,BYDAY,Description,Location)
        db.session.add(cform)
        db.session.commit()

        if not summary:
            flash('Class Name is required!')
        elif not DTStart:
            flash('Start Time is required!')
        elif not DTEnd:
            flash('End Time is required')
        elif not Duration:
            flash('Duration is required')
        elif not UNTIL:
            flash('UNTIL is required')
        elif not BYDAY:
            flash('BYDAY is required')
        else:
            messages.append({'Summary': summary, 'DTSTART': DTStart, 'DTEND': DTEnd, 'Duration': Duration, 'UNTIL': UNTIL, 'BYDAY': BYDAY, 'Description': Description, 'Location': Location})
            return redirect(url_for('index'))

    return render_template('create.html')

#Location should be kept not required alongside some others likely (description?)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)