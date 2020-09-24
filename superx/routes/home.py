from flask import render_template

from models import *


def home():

    products = Product.query.all()
    return render_template('home.html', products=products)


def logged_in():
   
    basket = db.session.query(Basket).get(1)

    return render_template('home-signedin.jinja2', basket=basket)

    