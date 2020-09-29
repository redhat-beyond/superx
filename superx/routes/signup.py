from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email
from flask import render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from models import *


class LoginForm(FlaskForm):
    email = StringField('אימייל', render_kw={"placeholder": "username@domain.com"},
                        validators=[InputRequired(), Length(min=3, max=50), Email("*בבקשה הכנס כתובת אימייל חוקית*")])
    password = PasswordField('סיסמה', render_kw={"placeholder": "******"}, validators=[InputRequired(),
                                                  Length(min=6, message="*בבקשה הכנס סיסמה המכילה לפחות 6 תווים*")])


class RegisterForm(FlaskForm):
    email = StringField('אימייל', render_kw={"placeholder": "username@domain.com"},
                        validators=[InputRequired(), Length(min=3, max=50), Email("*בבקשה הכנס כתובת אימייל חוקית*")])
    username = StringField('שם משתמש', validators=[InputRequired(), Length(min=3, max=10)])
    password = PasswordField('סיסמא', render_kw={"placeholder": "******"}, validators=[InputRequired(),
                                                  Length(min=6, message="*בבקשה הכנס סיסמה המכילה לפחות 6 תווים*")])


def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                return redirect(url_for('logged_in', name=request.args.get('form.username.data')))

    return render_template('login.jinja2', form=form)


def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hash_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(name=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(new_user)
        db.session.commit()

    return render_template('register.jinja2', form=form)
