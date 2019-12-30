from flask import Flask, render_template, url_for, request
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.getcwd() + '/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin')
def adminpage():
    return render_template("admin.html")

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if (request.method == 'POST') & ('myFile' in request.files):
        file = request.files['myFile']
        if (file.filename != '') & allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename, 'uploaded to ', os.path.join(app.config['UPLOAD_FOLDER'], filename))
    else:
        print(request.files)
    return render_template("admin.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')

