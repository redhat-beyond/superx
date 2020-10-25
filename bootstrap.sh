#!/usr/bin/env bash

# Update ubuntu
apt update

# Install virtualenv
apt install python3.8 python3-pip python3.8-ven -y 
pip3 install virtualenv  

# Create virtualenv
virtualenv superx --python=python3.8

# Create base working directory
source superx/bin/activate

# Install all dependencies
pip3 install flask Flask-SQLAlchemy Flask-Bootstrap SQLAlchemy flask_login flask_wtf pymysql pytest pytest-ordering requests bs4

export FLASK_APP=/vagrant/superx/app.py
export FLASK_ENV=development
flask run -h 0.0.0.0 -p 5000
