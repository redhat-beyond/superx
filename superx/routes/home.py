from flask import render_template

from models import *


def home():

    products = Product.query.all()
    return render_template('home.html', products=products)


def login():
    return render_template('login.html')

