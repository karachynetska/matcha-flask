from app import app
from flask import render_template, url_for, redirect, request
import html
import hashlib
import random
from datetime import datetime
import json
import re


@app.route('/register', methods=['POST'])
def register():
    login = html.escape(request.form['login'])
    password = request.form['password']
    firstname = html.escape(request.form['firstname'])
    lastname = html.escape(request.form['lastname'])
    email = html.escape(request.form['email'])
    birth_date = request.form['day'] + '/' + request.form['month'] + '/' + request.form['year']
    city = request.form['city']
    country = request.form['country']
    gender = request.form['gender']
    date_of_creation = datetime.now()


    if not firstname or lastname:
        return json.dumps({
            'ok': 'false',
            'error': "Please fill in all fields",
            'fields': ["firstname", "lastname"]
        })

    if len(firstname) < 2 or len(firstname) > 25:
        return json.dumps({
            'ok': 'false',
            'error': "Firstname length must be from 2 characters to 25",
            'fields': ["firstname"]
        })


    if len(lastname) < 2 or len(lastname) > 25:
        return json.dumps({
            'ok': 'false',
            'error': "Lastname length must be from 2 characters to 25",
            'fields': ["lastname"]
        })



    if not login:
        return json.dumps({
            'ok': 'false',
            'error': "Please fill in all fields",
            'fields': ["login"]
        })

    if len(login) < 2 or len(login) > 25:
        return json.dumps({
            'ok': 'false',
            'error': "Login length must be from 3 characters to 20",
            'fields': ["login"]
        })



    if not email:
        return json.dumps({
            'ok': 'false',
            'error': "Please fill in all fields",
            'fields': ["email"]
        })

    if not re.match("^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$", email.lower()):
        return json.dumps({
            'ok': 'false',
            'error': "Wrong email",
            'fields': ["email"]
        })



    if not password:
        return json.dumps({
            'ok': 'false',
            'error': "Please fill in all fields",
            'fields': ["password"]
        })

    if len(password) < 2 or len(password) > 25:
        return json.dumps({
            'ok': 'false',
            'error': "Password length must be from 8 characters to 16",
            'fields': ["password"]
        })

    if re.search("[a-zA-Z]+", password) is None or re.search("[0-9]+", password) is None:
        return json.dumps({
            'ok': 'false',
            'error': "Password is too weak",
            'fields': ["password"]
        })


    if not city:
        return json.dumps({
            'ok': 'false',
            'error': "Please fill in all fields",
            'fields': ["city"]
        })

    if not country:
        return json.dumps({
            'ok': 'false',
            'error': "Please fill in all fields",
            'fields': ["country"]
        })



    try:
        birth_date = datetime.strptime(birth_date, '%d/%b/%Y')
    except:
        return json.dumps({
            'ok': 'false',
            'error': "Wrong date",
            'fields': ["day", "month", "year"]
        })

    password_hash = hashlib.sha3_512(password)

    # standard avatar selection
    numb = random.randint(1, 13)
    avatar = str(numb) + '.png'
    avatar = '/static/avatars/' + avatar






