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


# @app.route('/cart/<items_list>', methods=['GET', 'POST'])
# def cart(items_list):
#     return home.cart(items_list)

@app.route("/addItem", methods=['GET', 'POST'])
def addItem():
    return home.addItem()


@app.route("/removeItem", methods=['GET', 'POST'])
def removeItem():
    return home.removeItem()

@app.route("/logout")
def logout():
    return signup.logout()

