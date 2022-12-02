from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager
import os
from os.path import join, dirname, realpath
from flask_sqlalchemy import SQLAlchemy

# login_manager = LoginManager()
app = Flask(__name__)
# login_manager.init_app(app)

# enable debugging mode
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:isu@localhost/test'

db = SQLAlchemy(app)

# Upload Folder
UPLOAD_FOLDER = app.static_folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER+'\\uploads\\'


class CForm(db.Model):
    __tablename__ = 'calendar'
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


@app.route("/", methods=['POST'])
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
    return redirect(url_for('index'))


with app.app_context():
    db.create_all()

if (__name__ == '__main__'):
    app.run(port=5000)
