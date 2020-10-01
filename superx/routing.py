from app import app
from routes import home, signup
from flask import request


@app.route('/')
def index():
    return home.home()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return signup.login()


@app.route('/register', methods=['GET', 'POST'])
def register():
    return signup.register()


@app.route('/inhome', methods=['GET', 'POST'])
def logged_in():
    return home.logged_in()


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    return home.cart()

  
@app.route("/logout")
def logout():
    return signup.logout()


@app.route('/addToCart', methods=['POST'])
def addItem():
    product_id = request.form.get('product_id')
    return home.add(product_id)

