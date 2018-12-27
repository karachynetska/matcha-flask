from app import app
from flask import render_template, url_for, redirect, request
import html
import hashlib
from datetime import datetime
import json


@app.route('/register', methods=['POST'])
def register():
    login = html.escape(request.form['login'])
    password = request.form['password']
    firstname = html.escape(request.form['firstname'])
    lastname = html.escape(request.form['lastname'])
    email = html.escape(request.form['email'])
    birth_date = request.form['day'] + '/' + request.form['month'] + '/' + request.form['year']
    print(birth_date)
    city = request.form['city']
    country = request.form['country']
    gender = request.form['gender']
    print(gender)

    birth_date = datetime.strptime(birth_date, '%d/%b/%Y')
    return "error"
