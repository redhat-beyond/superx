#!/usr/bin/env bash

apt-get update
apt-get install python3 python3-pip -y
pip3 install -r requirments.txt
# pip3 install flask Flask-SQLAlchemy SQLAlchemy pymysql Flask-WTF Flask-Bootstrap Flask_login pytest

export FLASK_APP=/vagrant/superx/app.py

export FLASK_ENV=development

flask run -h 0.0.0.0 -p 5000





export FLASK_APP=/vagrant/app.py

export FLASK_ENV=development

flask run -h 0.0.0.0 -p 5000