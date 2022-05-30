from flask import Flask, render_template, redirect, request, url_for, make_response
from datetime import datetime
import json

data: dict = None
app = Flask(__name__)


def update():
    with open("data.json", "w") as fout:
        fout.write(json.dumps(data, indent=4))


def get_data(field):
    global data
    if data is None:
        with open("data.json") as fin:
            data = json.loads(fin.read())
    return data.get(field)


def add_data(field_name, new_data):
    global data
    if data is None:
        with open("data.json") as fin:
            data = json.loads(fin.read())
    data[field_name].append(new_data)
    update()


def credentials_check(login_type, user_email, user_pass):
    """
    Returns the user id if credentials are correct, None otherwise
    """
    print(f"Checking credentials: {login_type}:'{user_email}'-'{user_pass}'")
    uid = None

    if login_type == "user":
        users = get_data("users")
        for x in users:
            if x["email"] == user_email and x["password"] == user_pass:
                uid = x["id"]
    else:
        users = get_data("employee")
        for x in users:
            if x["email"] == user_email and x["password"] == user_pass:
                uid = x["id"]
    print(uid)
    return uid


def check_login_type(login_type: str) -> bool:
    return login_type in ['employee', 'user', 'admin']


@app.route('/')
def main_page():
    cookie = request.cookies.get("user_id")
    if cookie is None:return render_template('mainPage.html', hotels=get_data('location'))
    cookie_comp = cookie.split('_')
    if cookie_comp[0] == 'employee':
        return redirect('/mainPage/employee')
    return render_template('mainPage.html', hotels=get_data('location'), id=cookie_comp[1])


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
        return redirect(url_for('userPage', login_type=account[0]))
    else:
        if check_login_type(login_type):
            return render_template("Login.html", login_type=login_type,
                                   retry=retry)
        else:
            print("NO SUCH PAGE WAS FOUND!")
            return render_template('ErrorPage.html', page=request.base_url), 404


@app.route("/logout")
def logout():
    response = make_response(render_template("Login.html", login_type="user", retry=False))
    response.set_cookie(key="user_id", value="", expires=datetime(1999, 12, 30))
    return response


@app.route("/mainPage/<string:login_type>")
def userPage(login_type):
    aux = request.cookies.get('user_id')
    if aux and check_login_type(login_type):
        return render_template(f"{login_type}_main.html")


@app.route("/check_signup", methods=['POST'])
def check_signup_data():
    for key, value in request.form.items():
        print(f"{key}: {value}")

    new_data = {key: value for key, value in request.form.items()}
    new_data["id"] = len(get_data("users"))
    add_data("users", new_data)

    return redirect(url_for('login', login_type='user'))


@app.route("/loginCheck", methods=['POST'])
def login_check():
    login_type = request.form.get('login_type')
    user_email = request.form.get('email')
    user_pass = request.form.get('passw')
    save_cookie = request.form.get('keep_logged_in')
    user_id = credentials_check(login_type, user_email, user_pass)

    if user_id is not None:
        response = make_response(render_template(f"{login_type}_main.html"))
        if save_cookie:
            response.set_cookie(key="user_id", value=f"{login_type}_{user_id}", expires=datetime(2034, 12, 30))
        else:
            response.set_cookie(key="user_id", value=f"{login_type}_{user_id}")
        return response

    return redirect(f'/login/{login_type}/FAILED')


@app.route("/acknowledge")
def ack_page():
    cookie = request.cookies.get("user_id")
    if cookie is None:
        return redirect(url_for("login", login_type='user'))
    cookie_fields = cookie.split("_")
    if cookie_fields[0] == 'user':
        return redirect(url_for("login", login_type='user'))
    else:
        employees = get_data("employee")
        x = None
        for e in employees:
            if e.get('id') == int(cookie_fields[1]):
                x = e
        print(x)

        hotel = x.get('hotel')
        reservations = [r for r in get_data('reservation') if r['hotel'] == hotel and r['status'] == 0]
        hx = None
        for h in get_data('location'):
            if h['id'] == hotel:
                hx = h
        return render_template("acknowledge.html", reservations=reservations, hotel=hx)


@app.route("/recvReservationStatus", methods=['POST'])
def manage_rez():
    for key, value in request.form.items():
        print(f'{key}: {value}')
        rez_id = int(key.split('_')[1])
        rez = None
        for r in get_data("reservation"):
            if r['id'] == rez_id:
                rez = r
        if value == 'True':
            rez['status'] = 1
        else:
            rez['status'] = 2
    update()
    return redirect("/mainPage/employee")


@app.route('/createReservation')
def res_page():
    cookie = request.cookies.get('user_id')
    if cookie is None:
        return redirect(url_for("login", logi_type='user'))
    cookie_f = cookie.split('_')
    hotel_id = -1
    hotel_data = None
    rezervari = None

    if cookie_f[0] == 'user':
        hotel_id = request.args.get('hotel')
    else:
        emp_id = int(cookie_f[1])
        for e in get_data('employee'):
            if e['id'] == emp_id:
                hotel_id = e['hotel']

    for h in get_data('location'):
        if h['id'] == hotel_id:
            hotel_data = h
    for r in get_data('reservation'):
        if r['hotel'] == hotel_id:
            rezervari = r
    return render_template("reservation.html", rezervari=rezervari,
                           hotel_data=hotel_data, user_type=cookie_f[0])


@app.route('/registerReservation', methods=['POST'])
def register_res():
    cookie_f = request.cookies.get('user_id').split('_')
    new_rez = {}
    if cookie_f[0] == 'employee':
        new_rez['user'] = -1
        new_rez['status'] = 1
    else:
        new_rez['user'] = int(cookie_f[1])
        new_rez['status'] = 0
    new_rez['from'] = request.form.get('from')
    new_rez['to'] = request.form.get('to')
    new_rez['nr_persoane'] = int(request.form.get('nr_persoane'))
    new_rez['hotel'] = request.form.get('hotel')
    new_rez['room_id'] = []
    for x, _ in request.form.items():
        if 'room_' in x:
            new_rez['room_id'].append(int(x.split('_')[1]))
    add_data('reservation', new_rez)
    return redirect('/')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('ErrorPage.html', page=request.base_url), 404
