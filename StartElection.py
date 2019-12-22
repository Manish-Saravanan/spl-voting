from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/vote')
def hello():
    return render_template("mainPage.html")

if __name__ == '__main__':
    app.run()