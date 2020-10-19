'''import app and routing modules
'''
from app import app
from routes import home, signup


@app.route('/', methods=['GET', 'POST'])
def index():
    '''
    main page route
    '''
    return home.home()


@app.route("/livesearch", methods=["POST", "GET"])
def livesearch():
    '''
    search route that does not reroute using jquery+ajax
    '''
    return home.livesearch()


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    logging in route
    '''
    return signup.login()


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''
    registering route
    '''
    return signup.register()


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    '''
    landing page for cart comparisons
    '''
    return home.cart()



@app.route("/addItem", methods=['GET', 'POST'])
def add_item():
    '''
    add an item route that does not reroute using jquery+ajax
    '''
    return home.addItem()

@app.route("/removeItem", methods=['GET', 'POST'])
def remove_item():
    '''
    remove an item route that does not reroute using jquery+ajax
    '''
    return home.removeItem()


@app.route("/logout")
def logout():
    '''
    logout route
    '''
    return signup.logout()
