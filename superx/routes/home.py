"""
import from flask and models and db
"""
from flask import render_template, request, session
from models import *
from app import db, supermarket_info_dictionary as sd


def home():
    """
    returns landing page of application
    """

    city_list = db.session.query(Branch.city).order_by(Branch.city).distinct().all()
    return render_template('home.html', city_list=city_list)


def cart():
    '''
    returns price comparison page with the users cart
    '''
    total_prices = {'mega' : { 'price' : 0, 'list' : []},
                'shufersal' : { 'price' : 0, 'list' : []},
                'victory': { 'price' : 0, 'list' : []}}
    for item in session['cart']:
        price_list_of_item = BranchPrice.query.filter_by(item_code=item['id']).all()
        for same_item in price_list_of_item:
            super_name = ''

            if same_item.chain_id == sd['mega']['chain_id']:
                super_name = 'mega'
            elif same_item.chain_id == sd['shufersal']['chain_id']:
                super_name = 'shufersal'
            elif same_item.chain_id == sd['victory']['chain_id']:
                super_name = 'victory'

            total_prices[super_name]['list'].append({
                "name": item['name'],
                "price": same_item.price
            })

            total_prices[super_name]['price'] += same_item.price

    return render_template('cart.html', total_prices=total_prices)


def livesearch():
    """
    returns search functin using jquery data and ajax so not to redirect
    """

    json_list_of_items = []

    # if search_res is empty string, return empty json
    search_res = request.form.get("input")
    if not search_res:
        return render_template('products_table.html', products=json_list_of_items)

    #pylint: disable=no-member
    products_list = \
    db.session.query(Product).order_by(Product.name).filter(Product.name.contains(search_res)).all()


    for item in products_list:
        json_list_of_items.append({
            "id": item.id,
            "name": item.name,
            "quantity": float(item.quantity),
            "unit_of_measure": item.unit_of_measure
        })
    return render_template('products_table.html', products=json_list_of_items)


def add_item():
    """
    adds item to cart using jquery to get the data and ajax so not to redirect
    """
    item = {'id': request.form.get('id'), 'name': request.form.get('name')}
    if 'cart' not in session:
        session['cart'] = []

    cart_list = session['cart']
    cart_list.append(item)
    session['cart'] = cart_list

    return ''


def remove_item():
    """
    removes item to cart using jquery to get the data and ajax so not to redirect
    """
    id_to_erase = request.form.get('id')
    if 'cart' not in session:
        return ''

    cart_list = session['cart']
    for i in enumerate(cart_list):
        if cart_list[i]['id'] == id_to_erase:
            del cart_list[i]
            break

    session['cart'] = cart_list

    return ''
