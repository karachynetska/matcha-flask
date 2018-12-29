from app import app, mail
from flask import render_template, url_for, redirect, request
import html
import hashlib
import random
from datetime import datetime
import json
import re
from app.models import user as user_model
from flask_mail import Message


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


# firstname and lastname
    if not (firstname or lastname):
        print('1')
        return json.dumps({
            'ok': False,
            'error': "Please fill in all fields",
            'fields': ["firstname", "lastname"]
        })

    if len(firstname) < 2 or len(firstname) > 25:
        print('2')
        return json.dumps({
            'ok': False,
            'error': "Firstname length must be from 2 characters to 25",
            'fields': ["firstname"]
        })


    if len(lastname) < 2 or len(lastname) > 25:
        print('3')
        return json.dumps({
            'ok': False,
            'error': "Lastname length must be from 2 characters to 25",
            'fields': ["lastname"]
        })


# login
    if not login:
        print('no login1')
        return json.dumps({
            'ok': False,
            'error': "Please fill in all fields",
            'fields': ["login"]
        })

    if len(login) < 2 or len(login) > 25:
        print('no login')
        return json.dumps({
            'ok': False,
            'error': "Login length must be from 3 characters to 20",
            'fields': ["login"]
        })


# email
    if not email:
        return json.dumps({
            'ok': False,
            'error': "Please fill in all fields",
            'fields': ["email"]
        })

    if not re.match("^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$", email.lower()):
        return json.dumps({
            'ok': False,
            'error': "Wrong email",
            'fields': ["email"]
        })


# password
    if not password:
        return json.dumps({
            'ok': False,
            'error': "Please fill in all fields",
            'fields': ["password"]
        })

    if len(password) < 2 or len(password) > 25:
        return json.dumps({
            'ok': False,
            'error': "Password length must be from 8 characters to 16",
            'fields': ["password"]
        })

    if re.search("[a-zA-Z]+", password) is None or re.search("[0-9]+", password) is None:
        return json.dumps({
            'ok': False,
            'error': "Password is too weak",
            'fields': ["password"]
        })

# city
    if not city:
        return json.dumps({
            'ok': False,
            'error': "Please fill in all fields",
            'fields': ["city"]
        })

# country
    if not country:
        return json.dumps({
            'ok': False,
            'error': "Please fill in all fields",
            'fields': ["country"]
        })

# birth_date
    try:
        birth_date = datetime.strptime(birth_date, '%d/%b/%Y')
    except:
        return json.dumps({
            'ok': False,
            'error': "Wrong date",
            'fields': ["day", "month", "year"]
        })

    password_hash = hashlib.sha3_512(password.encode('utf-8')).hexdigest()

# standard avatar selection
    numb = random.randint(1, 13)
    avatar = str(numb) + '.png'
    avatar = '/static/avatars/' + avatar


# token
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    token = hashlib.md5((login + date).encode('utf-8')).hexdigest()


    print(password_hash)

    user = user_model.save_user_to_db(login, password_hash, firstname, lastname, email, avatar, birth_date, city, country, token, gender)
    # user = user_model.save_user_to_db(login, 'password_hash', firstname, lastname, 'ema2il', 'dqd', 'qwedda', 'qq111',
    #                                   'qeff', 'dqdqd', 'dqwww')
    print(user)
    # if user:
    #     message = Message('Matcha registration', sender='matcha@project.unit.ua', recipients=[email])
    #     message.body = "Thank tou for registration in Matcha. To activate your accont please follow the link " + request.url_root + "activate?email=" + email + '&token=' + token
    #     message.html = "<p>Thank tou for registration in Matcha. To activate your accont please follow the <a href= " + request.url_root + "activate?email=" + email + '&token=' + token + ">link</a></p> "
    #     mail.send(message)
    return 'registered'


# @app.route('/activate')
# def activate_account():
#     email = request.args.get('email')
#     token = request.args.get('token')
#     if email is None or token is None:
#         return render_template('activate.html')
