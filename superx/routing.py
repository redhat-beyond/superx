from app import app
from routes import home, signup


@app.route('/', methods=['GET', 'POST'])
def index():
    return home.home()


@app.route("/livesearch", methods=["POST", "GET"])
def livesearch():
    return home.livesearch()


@app.route('/login', methods=['GET', 'POST'])
def login():
    return signup.login()


@app.route('/register', methods=['GET', 'POST'])
def register():
    return signup.register()


@app.route('/inhome', methods=['GET', 'POST'])
def logged_in():
    return home.logged_in()


@app.route('/cart/<string:items_code_string>', methods=['GET', 'POST'])
def cart(items_code_string):
    # convert string of items_code to list of items_code
    items_code_list = []
    one_product_string = ''
    for char in items_code_string:
        if char == '$':
            items_code_list.append(int(one_product_string))
            one_product_string = ''
            continue
        one_product_string += char
    return home.cart(items_code_list)


@app.route("/logout")
def logout():
    return signup.logout()
