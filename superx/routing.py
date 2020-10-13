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


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    return home.cart()

@app.route("/addItem", methods=['GET', 'POST'])
def addItem():
    return home.addItem()


@app.route("/removeItem", methods=['GET', 'POST'])
def removeItem():
    return home.removeItem()

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    return signup.logout()

