from flask import render_template, request, redirect, url_for

from models import *


def home():
    products = Product.query.order_by(Product.name).all()
    if request.method == "POST":
        # list of items code that the customer wants to compare
        items_list = []
        for item in request.form.keys():
            items_list.append(item)
        # TODO: Query the price of the items in items_list and send all the data to cart()
        return redirect(url_for("cart", items_list=items_list))
    else:
        return render_template('home.html', products=products)


def logged_in():
    return render_template('home-signedin.jinja2')


def cart(items_list):
    # TODO: add the db query for the products and send the info of each item and price to cart.html (three lists of products
    #  names & prices)

    return render_template('cart.html')
