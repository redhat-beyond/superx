from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from os import environ, path



app = Flask(__name__)
Bootstrap(app)

app.config.from_object('config.BaseConfig')
app.config['SECRET_KEY'] = 'aefguhw49t23465'
app.config['TESTING'] = False
FLASK_APP = environ.get('FLASK_APP')
FLASK_ENV = environ.get('FLASK_ENV')

# Database
SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

db = SQLAlchemy(app)
db.init_app(app)


from routing import *

if __name__ == '__main__':
    app.run(debug=True)
