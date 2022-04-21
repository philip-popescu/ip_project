from flask import Flask, render_template, redirect, request

app = Flask(__name__)


def check_login_type(login_type: str) -> bool:
    return login_type in ['employee', 'user']


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route("/login/<string:login_type>")
def login(login_type):
    if check_login_type(login_type):
        return render_template("Login.html", login_type=login_type)


@app.route("/mainPage/<string:login_type>")
def userPage(login_type):
    if check_login_type(login_type):
        return render_template("SignedIn.html", login_type=login_type)


@app.route("/loginCheck", methods=['GET', 'POST'])
def login_check():
    return NotImplementedError


@app.route("/2FCheck", methods=['GET', 'POST'])
def check_2f():
    return NotImplementedError

