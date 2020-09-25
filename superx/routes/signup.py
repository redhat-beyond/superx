from app import app
from routes import home
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired,  Length, ValidationError
from flask import render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from models import *
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user


def login():
    
    form = LoginForm()

    if form.validate_on_submit():
       user = User.query.filter_by(email=form.email.data).first()
       if user:
           if check_password_hash(user.password, form.password.data):
               return  redirect(url_for('logged_in', name=request.args.get('form.username.data')))


    return render_template('login.jinja2', form=form)

def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hash_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(name=form.username.data, email=form.email.data, password=hash_password) 
        db.session.add(new_user)
        db.session.commit()
        
    return render_template('register.jinja2', form=form)


class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(min=3, max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=3, max=10)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])


    def validate_email(self, email):
        user_object = User.query.filter_by(email=email.data).first()

        if user_object:
            raise ValidationError("email already exists, please login")

        import requests

        response = requests.get(
        "https://isitarealemail.com/api/email/validate",
        params = {'email': email.data})

        status = response.json()['status']
        if status != "valid":
            raise ValidationError("please put in an real email")








