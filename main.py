from flask import Flask
from flask import render_template, redirect, url_for, session, flash, abort
from flask import request
from flask_pymongo import PyMongo
from secrets import token_urlsafe

key = token_urlsafe(16)
print(key)


app = Flask(__name__)
app.secret_key = key

app.config["MONGO_URI"] = "mongodb://localhost:27017/userDBFlask"
mongodb_client = PyMongo(app)
db = mongodb_client.db

@app.route('/')
def index():
    if session.get("username"):
        return render_template("main.html", username=session.get("username"))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = db.users.find_one({'username': username})
    if user:
        if user['password'] == password:
            session["username"] = username
            return render_template("main.html", username=session.get("username"))
        else:
            return render_template('index.html', error='Invalid password')
    else:
        return render_template('register.html', error='Invalid username')

@app.get('/main')
def protected():
    if not session.get("username"):
        return redirect(url_for('index'))
    if session.get("username"):
        return render_template("main.html", username=session.get("username"))
    
    

@app.route('/registerform')
def registerform():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    surname = request.form['surname']
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']  
    db.users.insert_one({'surname': surname, 'name': name, 'username': username, 'password': password})
    session["username"] = username
    return render_template("main.html", username=session.get("username"))

if __name__ == '__main__':
    app.run(debug=True)

    