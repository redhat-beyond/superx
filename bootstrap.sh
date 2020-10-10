#!/usr/bin/env bash

# Update ubuntu
sudo apt-get update
# Install virtualenv
sudo apt-get install python-virtualenv

# Create virtualenv
virtualenv superx

# Create base working directory
source superx/bin/activate

# Install all dependencies
pip3 install flask Flask-SQLAlchemy Flask-Bootstrap SQLAlchemy flask_login flask_wtf pymysql pytest requests

export FLASK_APP=/vagrant/superx/app.py
export FLASK_ENV=development
flask run -h 0.0.0.0 -p 5000