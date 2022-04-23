from flask import Flask, render_template, redirect, request, url_for, make_response
from datetime import time, datetime

app = Flask(__name__)


def credentials_check(login_type, user_email, user_pass):
    """
    Returns the user id if credentials are correct, None otherwise
    """
    ret = 1782
    return ret


def check_login_type(login_type: str) -> bool:
    return login_type in ['employee', 'user', 'admin']


@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route("/login/<string:login_type>/FAILED")
@app.route("/login/<string:login_type>")
def login(login_type):
    aux = request.cookies.get('user_id')
    retry = 'FAILED' in request.base_url
    if aux:
        aux = aux.split('_')
        account = (aux[0], int(aux[1]))
        return redirect(url_for('main_page', login_type=account[0]))
    else:
        if check_login_type(login_type):
            return render_template("Login.html", login_type=login_type,
                                   retry=retry)
        else:
            print("NO SUCH PAGE WAS FOUND!")
            return render_template('ErrorPage.html', page=request.base_url), 404


@app.route("/mainPage/<string:login_type>")
def userPage(login_type):
    aux = request.cookies.get('user_id')
    if aux and check_login_type(login_type):
        return render_template("SignedIn.html", login_type=login_type)
    else:
        return render_template('ErrorPage.html', page=request.base_url), 404


@app.route("/loginCheck", methods=['GET', 'POST'])
def login_check():
    login_type = request.headers.get('login_type')
    user_email = request.headers.get('user_email')
    user_pass = request.headers.get('user_password')
    save_cookie = request.headers.get('keep_logged_in')
    user_id = credentials_check(login_type, user_email, user_pass)


    if user_id:
        response = make_response()
        if save_cookie:
            response.set_cookie(key="user", value=f"{login_type}_{user_id}", expires=datetime(2034, 12, 30))
        else:
            response.set_cookie(key="user", value=f"{login_type}_{user_id}")
        return response

    return redirect(url_for('/login', login_type=login_type))


@app.route("/2FCheck", methods=['GET', 'POST'])
def check_2f():
    return NotImplementedError


@app.route("/home/<string:name>")
def home(name):
    return render_template("welcome.html", name=name)
