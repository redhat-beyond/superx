from app import app
from routes import home
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired,  Length
from flask import render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import *

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=3, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=10)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])

@app.route('/')
def index():
    basket = db.session.query(Basket).get(1)
    return render_template('home.html', basket=basket)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
       user = User.query.filter_by(email=form.email.data).first()
       if user:
           if check_password_hash(user.password, form.password.data):
               return  '<h1>signed in!</h1>'
    
        

    return render_template('login.jinja2', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hash_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(name=form.username.data, email=form.email.data, password=hash_password) 
        db.session.add(new_user)
        db.session.commit()
        # return '<h1>' + form.username.data + ' ' + form.password.data + ' ' +  form.email.data + '</h1>'

    return render_template('register.jinja2', form=form)