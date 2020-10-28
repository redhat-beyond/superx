'''
importing login and form uses
and app
'''
import requests # pylint: disable=import-error
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from wtforms.fields.html5 import EmailField
from flask import render_template, redirect, url_for, session
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db # pylint: disable=import-error disable=no-name-in-module
from models import User, Branch # pylint: disable=import-error


class LoginForm(FlaskForm):
    '''
    login form flask using flaskform
    '''
    email = StringField('אימייל', render_kw={"placeholder": "username@domain.com"},
                        validators=[InputRequired(), Length(min=3, max=50)])
    password = PasswordField('סיסמה', render_kw={"placeholder": "******"},
    validators=[InputRequired(),Length(min=6,message="*בבקשה הכנס סיסמה המכילה לפחות 6 תווים*")])
    def validate_email(self,email): #pylint: disable=no-self-use
        '''
        validates that the user exists using email
        '''
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('*Email does not exist*')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    '''
    user loader fr Flask-Login
    '''
    return User.query.get(int(user_id))

def city_list():
    '''
    returns a city list for the field in the signup form so the user can pick there city
    '''
    citys = db.session.query(Branch.city).order_by(Branch.city).distinct().all() #pylint: disable=no-member
    city_list_tuples = []
    for city in citys:
        if city.city is None or city.city == 'unknown':
            continue
        city_list_tuples.append((city.city, city.city))
    return city_list_tuples


class RegisterForm(FlaskForm):
    '''
    register form flask using flaskform
    '''
    email = EmailField('אימייל', render_kw={"placeholder": "username@domain.com"},
                        validators=[InputRequired(), Length(min=3, max=50)])
    username = StringField('שם משתמש', validators=[InputRequired(), Length(min=3, max=10)])
    password = PasswordField('סיסמא', render_kw={"placeholder": "******"},
    validators=[InputRequired(),Length(min=6,message="*בבקשה הכנס סיסמה המכילה לפחות 6 תווים*")])
    confirm = PasswordField('ודא סיסמא', validators=[InputRequired(), EqualTo('password')])
    city = SelectField(u'עיר מגורים', choices=city_list(), validators=[InputRequired()])


    def validate_email(self, email): #pylint: disable=no-self-use
        '''
        checks that user does not exist and that email is legit
        '''
        user_object = User.query.filter_by(email=email.data).first()
        error_message = "*Email already exists*"
        if user_object:
            raise ValidationError(error_message)


        response = requests.get(
            "https://isitarealemail.com/api/email/validate",
            params={'email': email.data})

        status = response.json()['status']
        if status != "valid":
            raise ValidationError("*Please enter a valid email address*")


def login():
    '''
    logs in user(called from routes)
    '''
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if check_password_hash(user.password, form.password.data):
            login_user(user)
            session['city'] = user.city
            return redirect(url_for('index'))

    return render_template('login.jinja2', form=form)


def register():
    '''
    register in user(called from routes)
    '''
    form = RegisterForm()

    if form.validate_on_submit():
        hash_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(name=form.username.data,
        email=form.email.data,
        password=hash_password, city=form.city.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.jinja2', form=form)


@login_required
def logout():
    '''
    logout in user(called from routes)
    '''
    logout_user()
    return redirect(url_for('index'))
