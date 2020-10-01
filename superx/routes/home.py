from flask import render_template, session, redirect, request

from models import *


def home():
    products = Product.query.order_by(Product.name).all()
    session['cart'] = []
    return render_template('home.html', products=products)


def add(product_id):
    session['cart'].append(product_id)

    return "Nada"
def cart():
    return render_template('cart.html')
