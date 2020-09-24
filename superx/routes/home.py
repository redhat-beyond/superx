from flask import render_template

from models import *


def home():
    basket = db.session.query(Basket).get(1)
    return render_template('home.html', basket=basket)


def logged_in():
   
    basket = db.session.query(Basket).get(1)

    return render_template('home-signedin.jinja2', basket=basket)

    