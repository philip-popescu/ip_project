from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route('/')
def main():
    return render_template('index.html')


@app.route("/login/<string:login_type>")
def login(login_type):
    return redirect("/")
