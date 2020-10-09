from flask import render_template, request, redirect, url_for
from models import *
from app import supermarket_info_dictionary as sd


def home():
    if request.method == "POST":
        # Generate string of items_code separate by '$' sign.
        items_code_string = ''
        for item in request.form.keys():
            items_code_string += item
            items_code_string += '$'
        return redirect(url_for("cart", items_code_string=items_code_string))
    else:
        return render_template('home.html')


def cart(items_code_list):
    total_mega = 0
    total_shufersal = 0
    total_victory = 0
    mega_list = []
    shufersal_list = []
    victory_list = []

    for item_code in items_code_list:
        item_name = Product.query.filter_by(id=item_code).first()
        same_items_list = BranchPrice.query.filter_by(item_code=item_code).all()

        for same_item in same_items_list:
            if same_item.chain_id == sd['mega']['chain_id']:
                mega_list.append({
                    "name": item_name.name,
                    "price": same_item.price
                })
                total_mega += same_item.price

            elif same_item.chain_id == sd['shufersal']['chain_id']:
                shufersal_list.append({
                    "name": item_name.name,
                    "price": same_item.price
                })
                total_shufersal += same_item.price

            elif same_item.chain_id == sd['victory']['chain_id']:
                victory_list.append({
                    "name": item_name.name,
                    "price": same_item.price
                })
                total_victory += same_item.price

    return render_template('cart.html', total_mega=total_mega, total_shufersal=total_shufersal, total_victory=total_victory,
                           mega_list=mega_list, shufersal_list=shufersal_list, victory_list=victory_list)


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
