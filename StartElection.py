#!/usr/bin/python3

from flask import Flask, render_template, url_for, request, flash, redirect, get_flashed_messages
from databaseLibraries import *
from jinja2 import Environment
import os
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'key'

UPLOAD_FOLDER = os.getcwd() + '/static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

category = ['SPL-Boy', 'SPL-Girl', 'ASPL-Boy', 'ASPL-Girl']

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def landing():
    return redirect('/login')

@app.route('/login')
def login_view():
    Res = dict(map(lambda x:(x[0],x[1]), get_flashed_messages(with_categories=True)))
    try:
        return render_template("login.html", Msg=Res['401'])
    except KeyError:
        return render_template("login.html", Msg='')

@app.route('/adminlogin')
def admin_login():
    Res = dict(map(lambda x:(x[0],x[1]), get_flashed_messages(with_categories=True)))
    try:
        return render_template("adminlogin.html", Msg=Res['401'])
    except KeyError:
        return render_template("adminlogin.html", Msg='')

@app.route('/authadmin', methods=['POST'])
def admin_auth_task():
    form_data = request.form.to_dict()
    passcode = form_data.get('passwd')
    cp = GetAdminPass()
    if (cp != None) & (passcode == cp):
        data = GetCandidateData()
        flash('LoggedIn', '200')
        flash('', '401')
        return redirect('/admin')
    else:
        flash('Incorrect credentials.', '401')
        return redirect("/adminlogin")

@app.route('/admin')
def admin_view_1():
    Res = dict(map(lambda x:(x[0],x[1]), get_flashed_messages(with_categories=True)))
    try:
        if Res['200'] == 'LoggedIn':
            messg = Res['205'] if '205' in Res else ""
            flash('', '401')
            return render_template("admin-page.html", isElectionOpen = isElectionOpen, Msg = messg, total = TotalCount())
        else:
            return redirect('/adminlogin')
    except KeyError:
        return redirect('/adminlogin')

@app.route('/admin1')
def admin_view():
    Res = dict(map(lambda x:(x[0],x[1]), get_flashed_messages(with_categories=True)))
    data = GetCandidateData()
    cat = GetCat()
    try:
        if Res['200'] == 'LoggedIn':
            return render_template("admin.html", cat = category, data = data, GetPath = GetPath, isElectionOpen = isElectionOpen)
    except KeyError:
        return redirect('/adminlogin')

@app.route('/admin2')
def admin_openView():
    flash('LoggedIn', '200')
    return redirect('/admin1')

@app.route('/openVoting', methods=['POST'])
def open_Voting():
    form_data = request.form.to_dict()
    passcode = form_data.get('password')
    cp = GetAdminPass()
    if (cp != None) & (passcode == cp):
        ElectionOpen()
        flash('Election has been opened.', '205')
        flash('LoggedIn', '200')
        return redirect('/admin')
    else:
        flash('Incorrect credentials.', '401')
        return redirect("/confirmOpen")

@app.route('/confirmOpen')
def confirmOpen():
    Res = dict(map(lambda x:(x[0],x[1]), get_flashed_messages(with_categories=True)))
    try:
        return render_template("OpenConfirmation.html", Msg = Res['401'])
    except KeyError:
        return render_template("OpenConfirmation.html", Msg = '')

@app.route('/closeVoting', methods=['POST'])
def close_Voting():
    form_data = request.form.to_dict()
    passcode = form_data.get('password')
    cp = GetAdminPass()
    if (cp != None) & (passcode == cp):
        ElectionClose()
        flash('Election has been opened.', '205')
        flash('LoggedIn', '200')
        return redirect('/admin')
    else:
        flash('Incorrect credentials.', '401')
        return redirect("/confirmClose")

@app.route('/confirmClose')
def confirmClose():
    Res = dict(map(lambda x:(x[0],x[1]), get_flashed_messages(with_categories=True)))
    try:
        return render_template("CloseConfirmation.html", Msg = Res['401'])
    except KeyError:
        return render_template("CloseConfirmation.html", Msg = '')

@app.route('/resetVoting', methods=['POST'])
def reset_election():
    form_data = request.form.to_dict()
    passcode = form_data.get('password')
    cp = GetAdminPass()
    if (cp != None) & (passcode == cp):
        ResetElection()
        flash('Election has been opened.', '205')
        flash('LoggedIn', '200')
        return redirect('/admin')
    else:
        flash('Incorrect credentials.', '401')
        return redirect("/confirmReset")

@app.route('/confirmReset')
def confirmReset():
    Res = dict(map(lambda x:(x[0],x[1]), get_flashed_messages(with_categories=True)))
    try:
        return render_template("ResetConfirmation.html", Msg = Res['401'])
    except KeyError:
        return render_template("ResetConfirmation.html", Msg = '')

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    form_data = request.form.to_dict()
    candidateName = form_data.get('candidateName')
    category = form_data.get('category')
    if (request.method == 'POST') & ('myFile' in request.files):
        file = request.files['myFile']
        if (file.filename != '') & allowed_file(file.filename):
            filename = str(candidateName + str(datetime.datetime.now()) + '.' + file.filename.split('.')[-1]).replace(' ', '_')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            addCandidate(candidateName, filename, category)
        else:
            flash('LoggedIn', '200')
            return redirect('/admin1')
    else:
        flash('LoggedIn', '200')
        return redirect('/admin1')
    flash('LoggedIn', '200')
    data = GetCandidateData()
    return redirect('/admin1')

@app.route('/delete', methods=['POST'])
def deleteCandidate():
    form_data = request.form.to_dict()
    Cid = form_data.get('CID')
    delCandidate(Cid)
    flash('LoggedIn', '200')
    return redirect('/admin1')

@app.route('/electionResult')
def ViewResults():
    cat = GetCat()
    return render_template("ViewResults.html", cat = cat, GetResults = GetResults)

@app.route('/classsection', methods=['POST'])
def viewVoters():
    form_data = request.form.to_dict()
    cls = form_data.get('class_section')
    flash(cls, 'classsection')
    return redirect('/viewCredentials')

@app.route('/viewCredentials')
def ViewCred():
    Res = dict(map(lambda x:(x[0],x[1]), get_flashed_messages(with_categories=True)))
    try:
        return render_template("VotersList.html", cls = Res['classsection'], GetClassSection = GetClassSection, GetVoterDetails = GetVoterDetails)
    except KeyError:
        return render_template("VotersList.html", cls = '', GetClassSection = GetClassSection, GetVoterDetails = GetVoterDetails)

@app.route('/changepassword', methods=['POST'])
def changePassword():
    form_data = request.form.to_dict()
    cp = GetAdminPass()
    if form_data.get('oldpsswd') == cp:
        if form_data.get('newpsswd1') == form_data.get('newpsswd2'):
            ChangePasswd(form_data.get('newpsswd1'))
            flash('', 'changepassword')
            return "Successfully  changed."
        else:
            flash('Passwords do not match.', 'changepassword')
            return redirect('/changePswd')
    else:
        flash('Password does not match.', 'changepassword')
        return redirect('/changePswd')


@app.route('/changePswd')
def chngPasswd():
    Res = dict(map(lambda x:(x[0],x[1]), get_flashed_messages(with_categories=True)))
    try:
        return render_template("ChangePassword.html", Msg = Res['changepassword'])
    except KeyError:
        return render_template("ChangePassword.html", Msg = '')

@app.route('/vote', methods=['POST'])
def auth_task():
    if isElectionOpen()==1:
        form_data = request.form.to_dict()
        rlno = form_data.get('rollno')
        passcode = form_data.get('pass')
        cp = GetPass(rlno)
        Voted = hasVoted(rlno)
        if (cp != None) & (passcode == cp):
            if  (not Voted):
                cat = GetCat()
                flash('', '401')
                return render_template("Vote-page.html", cat = cat, GetCandidateNames = GetCandidateNames, GetPath = GetPath, rlno = rlno)
            else:
                flash('Aldready voted. You cannot vote again.', '401')
                return redirect("/login")
        else:
            flash('Incorrect roll number or passcode.', '401')
            return redirect("/login")
    elif isElectionOpen()==0:
        flash('Voting is not open.', '401')
        return redirect("/login")
    elif isElectionOpen()==2:
        flash('Voting is closed.', '401')
        return redirect("/login")
    else: return "The database has been affected"

@app.route('/backToLogin', methods=['POST'])
def backToLogin():
    return redirect("/login")

@app.route('/submitVote', methods=['POST'])
def submitVote():
    Votes = request.form.to_dict()
    cat = GetCat()
    CastVote(Votes, cat, Votes['rlno'])
    return render_template("Success.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
