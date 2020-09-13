from app import app
from routes import home

@app.route('/')
def index():
    return home.home()

@app.route('/login')
def login():
	return home.login()
