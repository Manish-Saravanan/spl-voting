from flask import Flask, render_template, url_for, request
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from databaseLibraries import GetCandidateData, GetCat, addCandidate
import datetime

UPLOAD_FOLDER = os.getcwd() + '/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
cat = ['SPL-Boy', 'SPL-Girl', 'ASPL-Boy', 'ASPL-Girl']

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin')
def adminpage():
    data = GetCandidateData()
    return render_template("admin.html", cat = cat, data = data)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form_data = request.form.to_dict()
    candidateName = form_data.get('candidateName')
    category = form_data.get('category')
    if (request.method == 'POST') & ('myFile' in request.files):
        file = request.files['myFile']
        if (file.filename != '') & allowed_file(file.filename):
            filename = candidateName + str(datetime.datetime.now()).split('-')[0] + '.' + file.filename.split('.')[-1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            addCandidate(candidateName, filename, category)
            
    data = GetCandidateData()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')

