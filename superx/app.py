from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object('config.BaseConfig')

db.init_app(app)

from routing import *

app.run(debug=False)
