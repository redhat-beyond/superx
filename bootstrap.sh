#!/usr/bin/env bash

sudo apt-get update 
sudo apt-get install python3 python3-pip -y
pip3 install virtualenv  
virtualenv superx
source superx/bin/activate
pip3 install flask Flask-SQLAlchemy Flask-Bootstrap SQLAlchemy flask_login flask_wtf pymysql pytest 

export FLASK_APP=/vagrant/superx/app.py

export FLASK_ENV=development

flask run -h 0.0.0.0 -p 5000
