from app import app
from routes import home, signup


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

