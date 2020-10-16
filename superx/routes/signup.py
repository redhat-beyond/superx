from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from wtforms.fields.html5 import EmailField
from flask import render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import *


class LoginForm(FlaskForm):
    email = StringField('אימייל', render_kw={"placeholder": "username@domain.com"},
                        validators=[InputRequired(), Length(min=3, max=50)])
    password = PasswordField('סיסמה', render_kw={"placeholder": "******"}, validators=[InputRequired(),
                                                                                       Length(min=6,
                                                                                              message="*בבקשה הכנס סיסמה המכילה לפחות 6 תווים*")])
   

    def validate_email(self, email):
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            raise ValidationError('*Email does not exist*')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class RegisterForm(FlaskForm):
    email = EmailField('אימייל', render_kw={"placeholder": "username@domain.com"},
                        validators=[InputRequired(), Length(min=3, max=50)])
    username = StringField('שם משתמש', validators=[InputRequired(), Length(min=3, max=10)])
    password = PasswordField('סיסמא', render_kw={"placeholder": "******"}, validators=[InputRequired(),
                                                                                       Length(min=6,
                                                                                              message="*בבקשה הכנס סיסמה המכילה לפחות 6 תווים*")])
    
    confirm = PasswordField('ודא סיסמא', validators=[DataRequired(), EqualTo('password')]) )

    def validate_email(self, email):
        user_object = User.query.filter_by(email=email.data).first()

        error_message = "*Email already exists*"
        if user_object:
            raise ValidationError(error_message)

        import requests

        response = requests.get(
            "https://isitarealemail.com/api/email/validate",
            params={'email': email.data})

        status = response.json()['status']
        if status != "valid":
            raise ValidationError("*Please enter a valid email address*")


def login():
    form = LoginForm()

    if form.validate_on_submit():
        if check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))

    return render_template('login.jinja2', form=form)


def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hash_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(name=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(new_user)
        db.session.commit()

    return render_template('register.jinja2', form=form)


@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
