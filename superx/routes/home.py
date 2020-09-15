from flask import render_template

from models import *


def home():
    basket = db.session.query(Basket).get(1)
    return render_template('home.html', basket=basket)


def login():
    return render_template('login.html')

# Snippet for creating data and pushing to db, use in the right context
# db.create_all()
#     db.session.commit()
#
#     products = [
#         Product(name='תפוח', quantity=20, is_weighted=True),
#         Product(name='תפוח', quantity=20, is_weighted=True),
#         Product(name='תפוח', quantity=20, is_weighted=True),
#     ]
#
#     db.session.add_all(products)
#     db.session.commit()
