from flask import render_template

from models import *


def home():
    basket = db.session.query(Basket).get(1)
    return render_template('home.html', basket=basket)


def login():
    return render_template('login.html')

