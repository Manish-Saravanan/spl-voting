from flask import Flask, render_template, url_for, request, flash, redirect, get_flashed_messages
from databaseLibraries import GetCat, GetPass, GetCandidateNames, CastVote, GetPath, hasVoted, GetCandidateData, addCandidate
from jinja2 import Environment
import os
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'key'

cat = GetCat()

UPLOAD_FOLDER = os.getcwd() + '/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

category = ['SPL-Boy', 'SPL-Girl', 'ASPL-Boy', 'ASPL-Girl']

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/admin')
def adminpage():
    data = GetCandidateData()
    return render_template("admin.html", cat = category, data = data)

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



@app.route('/login')
def login_view():
    try:
        return render_template("login.html", Msg=get_flashed_messages('401')[0][1])
    except IndexError:
        return render_template("login.html", Msg='')

@app.route('/authenticate', methods=['POST'])
def auth_task():
    form_data = request.form.to_dict()
    rlno = form_data.get('rollno')
    passcode = form_data.get('pass')
    cp = GetPass(rlno)
    Voted = hasVoted(rlno)
    if (cp != None) & (passcode == cp):
        if  (not Voted):
            return render_template("Vote-page.html", cat = cat, GetCandidateNames = GetCandidateNames, GetPath = GetPath, rlno = rlno)
        else:
            flash('Aldready voted. You cannot vote again.', '401')
            return redirect("/login")
    else:
        flash('Incorrect roll number or passcode.', '401')
        return redirect("/login")

@app.route('/submitVote', methods=['POST'])
def submitVote():
    Votes = request.form.to_dict()
    CastVote(Votes, cat, Votes['rlno'])
    flash('', '401')
    return redirect("/login")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')

