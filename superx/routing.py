"""
import app and routing modules
"""

from app import app
from routes import home, signup
from flask import session, request, render_template
from models import Branch


@app.route('/', methods=['GET', 'POST'])
def index():
    """
    main page route
    """
    return home.home()


@app.route("/livesearch", methods=["POST", "GET"])
def livesearch():
    """
    search route that does not reroute using jquery+ajax
    """
    return home.livesearch()


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    logging in route
    """
    return signup.login()


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    registering route
    """
    return signup.register()


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    """
    landing page for cart comparisons
    """
    return home.cart()


@app.route("/addItem", methods=['GET', 'POST'])
def add_item():
    """
    add an item route that does not reroute using jquery+ajax
    """
    return home.add_item()


@app.route("/removeItem", methods=['GET', 'POST'])
def remove_item():
    """
    remove an item route that does not reroute using jquery+ajax
    """
    return home.remove_item()


@app.route("/logout")
def logout():
    """
    logout route
    """
    return signup.logout()


@app.route('/city', methods=['GET', 'POST'])
def city():
    """
    adds city that was chosen, using jquery to get the data and ajax so not to redirect
    """
    # gets the city name from the user
    session['city'] = request.form.get('city')

    # entering the data of all branches in the city to branches_data
    branches_from_city = Branch.query.filter_by(city=session['city']).all()
    branches_data = []

    for branch in branches_from_city:

        # generates unique code for each branch -
        # this is an efficient way to produce a unique code for each branch
        branches_data.append(branch.chain_id+branch.id)

    # add branches_data to session
    session['branches_data'] = branches_data
    return ''


@app.route('/city_search', methods=['GET', 'POST'])
def city_search():
    """
    city serch route
    """
    return home.city_search()


@app.errorhandler(404)
def page_not_found():
    """
    route for 404 error handler
    """
    return render_template('404.html', title='404'), 404
