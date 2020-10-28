# Project Architecture
  In this document we will describe how the project is built, which technologies we used to built it and how they interact.
  - [Flow & Structure](#Flow-&-Structure)
  - [App run diagram](#App-run-diagram)

## Flow & Structure

<font color="blue"> _**Vagrant file-**_ </font>
 Defines the VM the app runs on. Works on ubuntu/bionic64 OS, triggers bootstrap.sh file.

<font color="blue"> _**bootstrap.sh-**_ </font>
 Updates the OS (if update exists), defines the app environment & installs dependencies. Then runs app.py on localhost:5000

<font color="blue"> _**app.py-**_ </font> 
Configures the app variables, configures the connection to the DB (based on config.py), runs all app routes (from routing.py) and defines a dictionary that will be used in the extractors scripts

## superx folder

<font color="blue"> _**information extractors-**_ </font>
 Two scripts which run on the relevant urls and extract data published by different food chains. branch_extractor gets the data of the different food branches, and item_extractor gets the products and their prices. The data is stored in the DB configured in app.py

<font color="blue"> _**models-**_ </font>
Contain _ init _.py, a file which determines the different tables columns defined in the DB. 
<br/> Post & Get methods to the DB requires importing models folders

<font color="blue"> _**routes-**_ </font>
 home.py & signup.py, define the app's functionality from user sign in to searching and comparing products. 
 - Rendering html files from templates dir.
 - Based on script.js & login_script.js from static/js

<font color="blue"> _**static-**_ </font>
 Images, CSS styling & JS scripts of the website

<font color="blue"> _**templates-**_ </font>
 Html & jinja2 files of the app's different pages

<font color="blue"> _**tests-**_ </font>
 Tests to the different functionality of the system. <br/> To run the tests- 
1. Activate the VM
2. Activate superx venv
3. Go to /vagrant/superx folder (not listed with dir command)
4. Run "python -m pytest"

## CI- .github/workflows
<font color="blue"> _**Pylint.yml-**_ </font>
 CI for running all relevant tests whenever a PR is made

### More files
<font color="blue"> _**README.md-**_ </font> description of the project's purpose, how it works and main contributors

<font color="blue"> _**DB Design.jpg-**_ </font> the data structure of the project including relationships between tables

<font color="blue"> _**Contributing.md-**_ </font>contribution guidelines to the project 

<font color="blue"> _**.vagrant folder-**_ </font> all relevant data to the VM

<font color="blue"> _**.gitignore-**_ </font> irrelevant files (github will ignore  them)


# App run diagram

![App run diagram](superx/static/img/app_run_diagram.JPG)
