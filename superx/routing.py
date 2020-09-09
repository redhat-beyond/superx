from app import app
from routes import home

@app.route('/')
def index_route():
    return home.home()

@app.route('/login')
def login():
	return home.login()