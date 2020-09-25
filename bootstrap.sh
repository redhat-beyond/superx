#!/usr/bin/env bash

apt-get update
apt-get install python3 python3-pip -y
sudo pip3 install Flask Flask-SQLAlchemy flask_login flask_wtf PyMySQL
# sudo pip3 install -r /vagrant/requirments.txt




export FLASK_APP=/vagrant/superx/app.py

export FLASK_ENV=development

flask run -h 0.0.0.0 -p 5000

