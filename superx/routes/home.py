from flask import render_template

from models import *


def home():
    products = Product.query.order_by(Product.name).all()
    return render_template('home.html', products=products)

