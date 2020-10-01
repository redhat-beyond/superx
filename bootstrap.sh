#!/usr/bin/env bash

apt-get update
apt-get install python3 python3-pip -y
sudo pip3 install virtualenv pathlib2 
virtualenv superx
source superx/bin/activate
sudo pip3 install flask Flask-SQLAlchemy Flask-Bootstrap SQLAlchemy flask_login flask_wtf pymysql pytest 

export FLASK_APP=/vagrant/superx/app.py

export FLASK_ENV=development

flask run -h 0.0.0.0 -p 5000

