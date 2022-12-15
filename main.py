from flask import Flask
from flask import render_template, redirect, url_for, session, flash, abort
from flask import request
from flask_pymongo import PyMongo
from secrets import token_urlsafe
from passlib.hash import pbkdf2_sha256
import functools
import http.client
import json


key = token_urlsafe(16)


app = Flask(__name__)
app.secret_key = key

app.config["MONGO_URI"] = "mongodb://localhost:27017/userDBFlask"
mongodb_client = PyMongo(app)
db = mongodb_client.db

def login_required(route):
    @functools.wraps(route)
    def route_wrapper(*args, **kwargs):
        if not session.get("username"):
            return redirect(url_for('index'))
        return route(*args, **kwargs)
    return route_wrapper




# HAUPTROUTEN
@app.route('/')
def index():
    if session.get("username"):
        return render_template("main.html", username=session.get("username"))
    return render_template('index.html')

@app.get('/main')
@login_required
def protected():
    #if not session.get("username"):
    #    return redirect(url_for('index'))
    return render_template("main.html", username=session.get("username"))
   

@app.route ('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# NUTZERVERWALTUNG

# Login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = db.users.find_one({'username': username})
    DB_API()
    if user:
        #if user['password'] == password:
        if pbkdf2_sha256.verify(password, user['password']):
            session["username"] = username
            return render_template("main.html", username=session.get("username"))
        else:
            flash ("Falsches Passwort")
            return render_template('index.html')
    else:
        flash ("User nicht bekannt")
        return render_template('register.html')
    


# Registrierung
    
@app.route('/registerform')
def registerform():
    return render_template('register.html')
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    user = db.users.find_one({'username': username})
    if user:
        flash("Nutzer schon angelegt, bitte einloggen")
        return render_template('index.html')
    else:
        surname = request.form['surname']
        name = request.form['name']
        username = request.form['username']
        password = pbkdf2_sha256.hash(request.form['password'])
    
        db.users.insert_one({'surname': surname, 'name': name, 'username': username, 'password': password})
        session["username"] = username
        flash("You are now registered and can log in", "success")
        return render_template("main.html", username=session.get("username"))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))



# API
def DB_API():
    def location():
        conn = http.client.HTTPSConnection("apis.deutschebahn.com")

        headers = {
        'DB-Client-Id': "7eec6e17aa2db2b09d76c490202112ac",
        'DB-Api-Key': "a3854011cb83292f31f11cfa8da36ffe",
        'accept': "application/json"
        }

        conn.request("GET", "/db-api-marketplace/apis/fahrplan/v1/location/Bonn", headers=headers)

        res = conn.getresponse()
        data = res.read()
        location = json.loads(data)
        code = location[0]["id"]
        timetable(code)

    def timetable(loc):
        conn = http.client.HTTPSConnection("apis.deutschebahn.com")
        print(loc)
        date = "2022-12-20"
        time = "T12:00"
        headers = {
        'DB-Client-Id': "7eec6e17aa2db2b09d76c490202112ac",
        'DB-Api-Key': "a3854011cb83292f31f11cfa8da36ffe",
        'accept': "application/json"
        }
        url = f"/db-api-marketplace/apis/fahrplan/v1/departureBoard/{loc}?date={date}{time}"
        print (url)
        conn.request("GET", url, headers=headers)

        res = conn.getresponse()
        data = res.read()
        result = json.loads(data)
        print(result)
    location()







if __name__ == '__main__':
    app.run(debug=True)

    