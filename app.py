from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route("/login/<string:login_type>")
def login(login_type):
    return render_template('login.html', login_type=login_type)
