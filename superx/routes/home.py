"""
import from flask and models and db
"""
# pylint: disable=redefined-outer-name, no-member, consider-using-enumerate

from flask import render_template, request, session, jsonify
from models import Branch, BranchPrice, Product
from app import db, supermarket_info_dictionary as sd

#  The amount of items to show the customer each search
# (more items = bigger delay from the input to the presentation)
NUMBER_OF_ITEMS_TO_SHOW = 20


def home():
    """
    returns landing page of application
    """
    city_list = db.session.query(Branch.city).order_by(Branch.city).distinct().all()
    return render_template('home.html', city_list=city_list,
                           number_of_items_to_show=NUMBER_OF_ITEMS_TO_SHOW)


def cart():
    """
    returns price comparison page with the users cart
    """

    # create generic dict for each chain
    total_prices = {key: {'price': 0, 'list': []} for key in sd}

    city = session['city']

    # loops on cart list
    for item in session['cart']:

        # create generic associate dict for each chain
        already_associate = {key: False for key in sd}

        # list of all BranchPrice objects data that have common id
        price_list_of_item = item['branch_price_items']

        # Loops on every BranchPrice objects with the same id as item
        for same_item in price_list_of_item:

            super_name = ''

            # sets the supermarket name
            for key in sd:
                if same_item['chain_id'] == sd[key]['chain_id']:
                    super_name = key

            if already_associate[super_name]:
                continue

            current_item_branch_id = same_item['branch_id']
            branches_list = Branch.query.filter_by(id=current_item_branch_id).all()

            # check if item belong to branch from this 'city' in this 'super_name'
            for branch in branches_list:

                if branch.city == city and branch.chain_id == sd[super_name]['chain_id'] \
                        and not already_associate[super_name]:
                    total_prices[super_name]['list'].append({
                        "name": item['name'],
                        "price": same_item['price'],
                        "num_items": item['num_items'],
                        "total_item_price": same_item['price'] * (int(item['num_items'])),
                        "associated": True
                    })
                    already_associate[super_name] = True
                    sum_price = total_prices[super_name]['list'][-1]['total_item_price']
                    total_prices[super_name]['price'] += sum_price
                    break

        for i in already_associate:
            if not already_associate[i]:
                total_prices[i]['list'].append({
                    "name": item['name'],
                    "price": 0,
                    "associated": False
                })

    return render_template('cart.html', total_prices=total_prices)


def livesearch():
    """
    returns search function using jquery data and ajax so not to redirect
    """

    products = []
    search_res = request.form.get("input").strip()
    branches_code_list = session['branches_data']

    # if search_res is empty string, skip and return empty products list
    if search_res:

        # query all products from DB that contains search_res in their name
        products_list = db.session.query(Product).order_by(Product.name) \
            .filter(Product.name.contains(search_res)).all()

        for item_count, item in enumerate(products_list):

            # after NUMBER_OF_ITEMS_TO_SHOW items added break from the loop
            if item_count == NUMBER_OF_ITEMS_TO_SHOW:
                break

            # query all the BranchPrice objects associated with the item variable
            branch_price_list_of_item = BranchPrice.query.filter_by(item_code=item.id).all()

            for branch_price_item in branch_price_list_of_item:

                # save the unique code that composed of branch_id number plus chain_id number
                unique_branch_code = (branch_price_item.chain_id + branch_price_item.branch_id)

                # check if the BranchPrice object belongs to branch located in city
                # if so adding the product to the products list
                if unique_branch_code in branches_code_list:
                    products.append({
                        "id": item.id,
                        "name": item.name,
                        "quantity": float(item.quantity),
                        "num_items": 1,
                        "unit_of_measure": item.unit_of_measure
                    })
                    item_count += 1
                    break

    return render_template('products_table.html', products=products)


# This method is used by addItem function in static/js/script.js
def add_item():
    """
    adds item to cart using jquery to get the data and ajax so not to redirect
    """

    item_code = request.form.get('id')
    branch_price_item_list = BranchPrice.query.filter_by(item_code=item_code).all()
    item = {'id': item_code, 'name': request.form.get('name'),
            'num_items': request.form.get('num_items'),
            'branch_price_items': [{'chain_id': item.chain_id,
                                    'branch_id': item.branch_id,
                                    'price': float(item.price)}
                                   for item in branch_price_item_list]
            }

    # If there are no chosen products yet initiate cart in session object
    if 'cart' not in session:
        session['cart'] = []

    cart_list = session['cart']
    cart_list.append(item)
    session['cart'] = cart_list

    was_city_chosen = bool('city' in session)

    return jsonify({'was_city_chosen': was_city_chosen})


def remove_item():
    """
    removes item to cart using jquery to get the data and ajax so not to redirect
    """
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


def city_search():
    """
    renders the city list for the user if it wants to cahnge a city from his city
    """
    city_list = db.session.query(Branch.city).order_by(Branch.city).distinct().all()
    return render_template('city_list.html', city_list=city_list)


def update_num_items():
    """
    renders number of items chosen for a product according to user's input
    """
    id_to_update = request.form.get('id')
    num_items = request.form.get('num_items')

    cart_list = session['cart']
    for item in cart_list:
        if item['id'] == id_to_update:
            item['num_items'] = num_items
            break
    session['cart'] = cart_list

    return ''
