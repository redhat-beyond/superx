from flask import render_template
 
def home():
    return render_template('home.html')

def login():
	return render_template('login.html')