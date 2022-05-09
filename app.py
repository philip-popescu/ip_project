from flask import make_response
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

# WEBSITE_HOSTNAME exists only in production environment
if 'WEBSITE_HOSTNAME' not in os.environ:
   # local development, where we'll use environment variables
   print("Loading config.development and environment variables from .env file.")
   app.config.from_object('azureproject.development')
else:
   # production
   print("Loading config.production.")
   app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Initialize the database connection
db = SQLAlchemy(app)

# Enable Flask-Migrate commands "flask db init/migrate/upgrade" to work
migrate = Migrate(app, db)

# Create databases, if databases exists doesn't issue create
# For schema changes, run "flask db migrate"
db.create_all()
db.session.commit()


def credentials_check(login_type, user_email, user_pass):
    """
    Returns the user id if credentials are correct, None otherwise
    """
    print(f"Checking credentials: {login_type}:'{user_email}'-'{user_pass}'")
    uid = None
    if login_type == "user":
        from models import Client
        cli = Client.query.filter(Client.email == user_email, Client.password == user_pass).one_or_none()
    else:
        from models import Angajat
        cli = Angajat.query.filter(Angajat.email == user_email, Angajat.password == user_pass).one_or_none()
    if cli:
        uid = cli.id
    return uid


def check_login_type(login_type: str) -> bool:
    return login_type in ['employee', 'user', 'admin']


@app.route('/')
def main_page():
    return render_template('image.html')


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


@app.route("/logout")
def logout():
    return redirect("/login/user")


@app.route("/mainPage/<string:login_type>")
def userPage(login_type):
    aux = request.cookies.get('user_id')
    if aux and check_login_type(login_type):
        return render_template("SignedIn.html", login_type=login_type)
    else:
        return render_template('ErrorPage.html', page=request.base_url), 404


@app.route("/check_signup", methods=['POST'])
@csrf.exempt
def check_signup_data():
    for key, value in request.form.items():
        print(f"{key}: {value}")

    return redirect(url_for('login', login_type='user'))


@app.route("/loginCheck", methods=['POST'])
@csrf.exempt
def login_check():
    login_type = request.form.get('login_type')
    user_email = request.form.get('user_email')
    user_pass = request.form.get('user_password')
    save_cookie = request.form.get('keep_logged_in')
    user_id = credentials_check(login_type, user_email, user_pass)

    if user_id:
        response = make_response(render_template("2FactorId.html"))
        if save_cookie:
            response.set_cookie(key="user", value=f"{login_type}_{user_id}", expires=datetime(2034, 12, 30))
        else:
            response.set_cookie(key="user", value=f"{login_type}_{user_id}")
        return response

    return redirect(f'/login/{login_type}/FAILED')


@app.route("/2FCheck", methods=['GET', 'POST'])
def check_2f():
    return NotImplementedError


@app.route("/home/<string:name>")
def home(name):
    return render_template("welcome.html", name=name)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('ErrorPage.html', page=request.base_url), 404
