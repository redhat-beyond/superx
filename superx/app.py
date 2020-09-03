from flask import Flask  

app = Flask(__name__) 

from routing import *

app.run(debug = True)
