from flask import Flask
from flask import render_template, redirect, url_for
from flask import request
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/userDBFlask"
mongodb_client = PyMongo(app)
db = mongodb_client.db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main')
def main():
    return render_template('main.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = db.users.find_one({'username': username})
    if user:
        if user['password'] == password:
            return redirect(url_for('main'))
            #return "Welcome " + username
        else:
            return 'Invalid password'
    else:
        return 'Invalid username'


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
    return 'user added'

if __name__ == '__main__':
    app.run(debug=True)

    