from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cc30d0a491daf6a4ba282e9ea5f9dcfc994cb4b86d66f531'

#Messages is just a name, I was gonna switch it to classes
# but I couldn't get it to work for the time being, so keep it for now
# unless you know how to fix it
messages = [
            ]

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

        if not summary:
            flash('Class Name is required!')
        elif not DTStart:
            flash('Start Time is required!')
        elif not DTEnd:
            flash('End Time is required')
        else:
            messages.append({'Summary': summary, 'DTSTART': DTStart, 'DTEND': DTEnd, 'Duration': Duration, 'UNTIL': UNTIL, 'BYDAY': BYDAY, 'Description': Description, 'Location': Location})
            return redirect(url_for('index'))

    return render_template('create.html')

#Location should be kept not required alongside some others likely (description?)