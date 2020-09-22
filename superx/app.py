from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap



app = Flask(__name__)
Bootstrap(app)
app.config.from_object('config.BaseConfig')
app.config['SECRET_KEY'] = 'aefguhw49t23465'

db = SQLAlchemy(app)
db.init_app(app)

from routing import *

# app.run(debug=True)
