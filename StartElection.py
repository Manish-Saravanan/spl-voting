from flask import Flask, render_template, url_for, request 

app = Flask(__name__)

data = [["SPL-Girl", [["candidate1", "path1.jpg", "no of votes"],["candidate2", "path2.jpg", "no of votes"],["candidate3", "path3.jpg", "no of votes"],["candidate4", "path4.jpg", "no of votes"],["candidate5", "path2.jpg", "no of votes"]]],
        ["SPL-Boy", [["candidate1", "path1.jpg", "no of votes"],["candidate2", "path2.jpg", "no of votes"],["candidate3", "path3.jpg", "no of votes"],["candidate4", "path4.jpg", "no of votes"]]],
        ["ASPL-Boy", [["candidate1", "path1.jpg", "no of votes"],["candidate2", "path2.jpg", "no of votes"],["candidate3", "path3.jpg", "no of votes"],["candidate4", "path4.jpg", "no of votes"]]],
        ["ASPL-Girl", [["candidate1", "path1.jpg", "no of votes"],["candidate2", "path2.jpg", "no of votes"],["candidate3", "path3.jpg", "no of votes"],["candidate4", "path4.jpg", "no of votes"]]]]

credentials = {'123456':"54321", '567890':"09876"}



@app.route('/login')
def login_view():
    return render_template("login.html")

@app.route('/vote')
def voting():
    return render_template("Vote-page.html", data = data)

@app.route('/submit', methods=['POST'])
def submit():
    votes = request.form.getlist("SPL-Girl")
    print(request.form)
    return render_template("login.html")

@app.route('/authenticate', methods=['POST'])
def auth_task():
    usnnum = request.form.getlist('usnno')
    passcode = request.form.getlist('pass')
    if usnnum[0] in credentials:
        if credentials[usnnum[0]]==passcode[0]:
            return render_template("Vote-page.html", data = data)
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")

if __name__ == '__main__':
    app.run()