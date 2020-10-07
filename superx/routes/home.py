from flask import render_template, request, redirect, url_for, session
from models import *


def home():
    products = Product.query.order_by(Product.name).all()
   
    return render_template('home.html', products=products)


def cart(items_list):
    # TODO: add the db query for the products and send the info of each item and price to cart.html (three lists of products
    #  names & prices)

    return render_template('cart.html')


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
