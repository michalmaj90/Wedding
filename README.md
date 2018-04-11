## Wedding Application

**Version 1.0.0**

*This is my final project, finishing my participation in "Back-end: Python" course in CodersLab School of programming.*


## Why this project?
I created this app, due to my wedding celebration which is taking place this year. This version should help us to collect infos about our guests and enable our guests to know everything about our celebration.

## Getting started
Before you run the app you should:
- run or create your virtual environment,
- go to the destination, where you want this app to run
- clone this repo by copying its URL and putting it into a "git clone" command

## How to run the app
After you cloned the repo to the local file:
- create database called "wedding" by typing: 
"CREATE DATABASE wedding CHARACTER SET utf8 COLLATE utf8_general_ci;"
- get into the project folder in your terminal
- install django by using "pip install Django" command in your terminal
- install necessary requirements by typing "pip install -r requirements.txt" in your terminal
- type "python manage.py migrate" in your terminal
- type "python manage.py makemigrations" to make sure nothing else left to migrate
- if any migrations were done type: "python manage.py migrate" again , but if "no changes detected" type: "python manage.py runserver"
- get into the link, that appeared and add "/hello" in the end
- if your server is busy type: "sudo fuser -k localhost_number/tcp"


