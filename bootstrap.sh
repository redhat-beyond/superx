#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install python3
sudo apt-get install python3-pip -y
sudo pip3 install flask

export FLASK_APP=/vagrant/app.py

export FLASK_ENV=development

flask run -h 0.0.0.0 -p 5000
