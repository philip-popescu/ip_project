from flask import Flask, render_template, redirect

app = Flask(__name__)


def check_login_type(login_type: str) -> bool:
    return login_type in ['employee', 'user']


@app.route('/')
def main():
    return render_template('index.html')


@app.route("/login/<string:login_type>")
def login(login_type):
    if check_login_type(login_type):
        return redirect("/")


@app.route("/user/<string:login_type>")
def user(login_type):
    if check_login_type(login_type):
        return render_template("SignedIn.html", login_type=login_type)
