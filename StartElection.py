from flask import Flask, render_template, url_for, request
from databaseLibraries import GetCat, GetPass, GetCandidateNames, CastVote, GetPath, hasVoted
from jinja2 import Environment

app = Flask(__name__)

cat = GetCat()

@app.route('/login')
def login_view():
    return render_template("login.html")

@app.route('/authenticate', methods=['POST'])
def auth_task():
    form_data = request.form.to_dict()
    rlno = form_data.get('rollno')
    passcode = form_data.get('pass')
    cp = GetPass(rlno)
    Voted = hasVoted(rlno)
    if (cp != None) & (passcode == cp) & (not Voted):
        return render_template("Vote-page.html", cat = cat, GetCandidateNames = GetCandidateNames, GetPath = GetPath, rlno = rlno)
    else:
        return render_template("login.html")

@app.route('/submit', methods=['POST'])
def submit():
    Votes = request.form.to_dict()
    CastVote(Votes, cat, Votes['rlno'])
    return render_template("login.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')

