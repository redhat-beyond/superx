from flask import render_template, request, redirect, url_for, session
from models import *
from app import supermarket_info_dictionary as sd


def home():
    # products = Product.query.order_by(Product.name).all()
   
    return render_template('home.html')


class Item(object):
    def __init__(self, item_code, item_name, chain_id, branch_id, price):
        pass


def cart():
    total_prices = {'mega' : { 'price' : 0, 'list' : []}, 'shufersal' : { 'price' : 0, 'list' : []}, 'victory': { 'price' : 0, 'list' : []}}
    for item in session['cart']:
        price_list_of_item = BranchPrice.query.filter_by(item_code=item['id']).all()

        for same_item in price_list_of_item:
            if same_item.chain_id == sd['mega']['chain_id']:
                total_prices['mega']['list'].append({
                    "name": item['name'],
                    "price": same_item.price
                })
                total_prices['mega']['price'] += same_item.price
            
            elif same_item.chain_id == sd['shufersal']['chain_id']:
                total_prices['shufersal']['list'].append({
                    "name": item['name'],
                    "price": same_item.price
                })
                total_prices['shufersal']['price'] += same_item.price

            elif same_item.chain_id == sd['victory']['chain_id']:
                total_prices['victory']['list'].append({
                    "name": item['name'],
                    "price": same_item.price
                })
                total_prices['victory']['price'] += same_item.price

    return render_template('cart.html', total_prices=total_prices)


def livesearch():
    
    json_list_of_items = []

    # if search_res is empty string, return empty json
    search_res = request.form.get("input")
    if not search_res:
        return render_template('products_table.html', products=json_list_of_items)

    products_list = db.session.query(Product).filter(Product.name.contains(search_res)).all()

    for item in products_list:
        json_list_of_items.append({
            "id": item.id,
            "name": item.name,
            "quantity": float(item.quantity),
            "unit_of_measure": item.unit_of_measure
        })
    return render_template('products_table.html', products=json_list_of_items)


def addItem():
    item = {'id' : request.form.get('id'), 'name' : request.form.get('name')}
    if 'cart' not in session:
        session['cart'] = [] 
    
    cart_list = session['cart']
    cart_list.append(item)
    session['cart'] = cart_list  
    
    return ''

def removeItem():
    id_to_erase = request.form.get('id')
    if 'cart' not in session:
        return ''
    
    cart_list = session['cart']
    for i in range(len(cart_list)): 
        if cart_list[i]['id'] == id_to_erase: 
            del cart_list[i] 
            break
    
    session['cart'] = cart_list  
    
    return ''
