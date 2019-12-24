from flask import Flask, render_template, url_for

app = Flask(__name__)

data = [["SPL-Girl", [["candidate1", "path1", "no of votes"],["candidate2", "path2", "no of votes"],["candidate3", "path3", "no of votes"],["candidate4", "path4", "no of votes"]]],
        ["SPL-Boy", [["candidate1", "path1", "no of votes"],["candidate2", "path2", "no of votes"],["candidate3", "path3", "no of votes"],["candidate4", "path4", "no of votes"]]],
        ["ASPL-Boy", [["candidate1", "path1", "no of votes"],["candidate2", "path2", "no of votes"],["candidate3", "path3", "no of votes"],["candidate4", "path4", "no of votes"]]],
        ["ASPL-Girl", [["candidate1", "path1", "no of votes"],["candidate2", "path2", "no of votes"],["candidate3", "path3", "no of votes"],["candidate4", "path4", "no of votes"]]]]


@app.route('/login')
def hello():
    return render_template("login.html", ref1= "/css", ref2="/vote")


'''
@app.route('/css')
def index():        
    return render_template("style.css", _external=True)
'''

@app.route('/vote')
def voting():        
    return render_template("Vote-page.html", data = data)



if __name__ == '__main__':
    app.run()