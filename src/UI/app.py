from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager
import os
from os.path import join, dirname, realpath

# login_manager = LoginManager()
app = Flask(__name__)
# login_manager.init_app(app)

# enable debugging mode
app.config["DEBUG"] = True

# Upload Folder
UPLOAD_FOLDER = app.static_folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER+'\\uploads\\'


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
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        # save the file
    return redirect(url_for('index'))

if (__name__ == '__main__'):
    app.run(port = 5000)