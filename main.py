from flask import Flask
from flask import render_template, redirect, url_for, session, flash, abort
from flask import request
import pymongo
from secrets import token_urlsafe
from passlib.hash import pbkdf2_sha256
import functools
import http.client
import json
from logic import *


key = token_urlsafe(16)


app = Flask(__name__)
app.secret_key = key

uri = "mongodb+srv://<user_string>"
mongodb_client = pymongo.MongoClient(uri)
resultdb = mongodb_client["mobi_user"]["mobi_user"].find() 
db = mongodb_client["mobi_user"]["mobi_user"].db


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
def input():
    #if not session.get("username"):
    #    return redirect(url_for('index'))
    return render_template("main.html", username=session.get("username"))
   

@app.route ('/dashboard', methods=['POST'])
@login_required
def dashboard():
    start = request.form['start']
    ziel = request.form['ziel']
    time= request.form['departure']
    date= request.form['date']
    mode = request.form.getlist('mode')
    selection = request.form.get('selection')
    datetime = date + " " + time
    
    if start and ziel and time and datetime and mode:
        result = selectSource(start, ziel, mode, datetime, selection)
        print("Abruf erfolgreich")
        print(result)
        return render_template('dashboard.html', result=result)
    else:
        flash("Bitte alle Felder ausfüllen")
        return render_template('main.html', username=session.get("username"))
      


# NUTZERVERWALTUNG

# Login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = db.mobi_user.find_one({'username': username})
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
    user = db.mobi_user.find_one({'username': username})
    if user:
        flash("Nutzer schon angelegt, bitte einloggen")
        return render_template('index.html')
    else:
        surname = request.form['surname']
        name = request.form['name']
        username = request.form['username']
        password = pbkdf2_sha256.hash(request.form['password'])
    
        db.mobi_user.insert_one({'surname': surname, 'name': name, 'username': username, 'password': password})
        session["username"] = username
        flash("You are now registered and can log in", "success")
        return render_template("main.html", username=session.get("username"))

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

