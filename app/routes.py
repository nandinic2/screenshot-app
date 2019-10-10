from app import app
from flask import Flask, request, send_file, url_for, render_template, redirect
from flask_bootstrap import Bootstrap
from app.models import model
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import pyautogui
import time

from flask_pymongo import PyMongo

app.config['SECRET_KEY'] = 'sanskriti2012'
app.config['MONGO_URI'] = 'mongodb+srv://admin:teesi5o1gOex2h5G@cluster0-n5tzk.mongodb.net/pictures?retryWrites=true&w=majority'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/2020nchakravorty/Desktop/screenshottest.db'


db = SQLAlchemy(app)

mongo = PyMongo(app)
Bootstrap(app)

#the login form
# class LoginForm(FlaskForm):
#     #username part of login
#     username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
#     password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
#     remember = BooleanField('remember me')
#
# class RegisterForm(FlaskForm):
#     username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
#     email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
#     password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
#
# class User(db.Model):
#     id = db.Column('id', db.Integer, primary_key=True)
#     username = db.Column(db.String(15), unique=True)
#     email = db.Column(db.String(50), unique=True)
#     password = db.Column(db.String(80))
#
# @app.route('/')
# def index():
#     return render_template('index.html')
#
# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     form = LoginForm()
#     #checks to see if form has been submitted
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user:
#             #if user logged in correctly, redirect to the dashboard
#             if user.password == form.password.data:
#                 return redirect(url_for('dashboard'))
#         #if user doesn't exist or login incorrect
#         return '<h1> Invalid username or password </h1>'
#         #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
#     return render_template('login.html', form = form)
#
# @app.route('/signup', methods=['POST', 'GET'])
# def signup():
#     form = RegisterForm()
#     #allow new user to be created
#     if form.validate_on_submit():
#         new_user = User(username=form.username.data, email=form.email.data, password=form.password.data)
#         db.session.add(new_user)
#         try:
#             db.session.commit()
#             return '<h1>New user has been created!</h1>'
#         except IntegrityError:
#             db.session.rollback()
#
#
#         #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
#     return render_template('signup.html', form=form)
# 
# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')
#
# if __name__ == '__main__':
#     app.run(debug=True)



@app.route('/input', methods=["GET"])
def input():
    return render_template('input.html')

@app.route('/create',  methods = ["POST"])
def create():
    if "screenshot" in request.files:
        screenshot = request.files["screenshot"]
        mongo.save_file(screenshot.filename, screenshot)
        mongo.db.pictures.insert({'username': request.form.get('username'),'screenshot':screenshot.filename})
    return '''<a href='index'>Enter new screenshot</a>
    <a href='/profile'>View past screenshots</a>'''

@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

@app.route('/profile/<username>')
def profile(username):
    pictures = list(mongo.db.pictures.find({}))
    print(pictures)
    return render_template('profile.html', pictures = pictures, username = username)

@app.route('/screenshot')
def screenshot():
    pictures = list(events.find({}))
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    img = pyautogui.screenshot()
    time.sleep(2)
    return send_file(img)

@app.route('/deleteAll', methods = ['Get','Post'])
def deleteAll():

    userdata = dict(request.form)
    #names password collected from form as password
    password = userdata['password']
    if password == "clearit!":
        #connects to the database
        collection = mongo.db.pictures
        #deletes all entries in the database
        collection.delete_many({})
        #loads deleteAll.html
        return render_template("deleteAll.html", password = password)
    else:
        return "incorrect password"
