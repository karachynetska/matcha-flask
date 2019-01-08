from app import app, mail
from flask import render_template, url_for, redirect, request, session
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
    password = html.escape(request.form['password'])
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
        return json.dumps({
            'ok': False,
            'error': "Please fill in all fields",
            'fields': ["firstname", "lastname"]
        })

    if len(firstname) < 2 or len(firstname) > 25:
        return json.dumps({
            'ok': False,
            'error': "Firstname length must be from 2 characters to 25",
            'fields': ["firstname"]
        })


    if len(lastname) < 2 or len(lastname) > 25:
        return json.dumps({
            'ok': False,
            'error': "Lastname length must be from 2 characters to 25",
            'fields': ["lastname"]
        })


# login
    if not login:
        return json.dumps({
            'ok': False,
            'error': "Please fill in all fields",
            'fields': ["login"]
        })

    if len(login) < 2 or len(login) > 25:
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

# Сheck for user availability
    login_exists = user_model.login_exists(login)
    print(login_exists)
    if login_exists:
        return json.dumps({
            'ok': False,
            'error': "User with this login already exists",
            'fields': ["login"]
        })

    email_exists = user_model.email_exists(email)
    if email_exists:
        return json.dumps({
            'ok': False,
            'error': "User with this email already exists",
            'fields': ["email"]
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

# standard avatar and background selection
    numb = random.randint(1, 13)
    avatar = str(numb) + '.png'
    avatar = '/static/avatars/' + avatar
    background = str(numb) + '.jpg'
    background = '/static/backgrounds/' + background



# token
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    token = hashlib.md5((login + date).encode('utf-8')).hexdigest()


# saving user to db and sending email
    user = user_model.save_user_to_db(login, password_hash, firstname, lastname, email, avatar, background, birth_date, city, country, token, gender)
    if user:
        message = Message('Matcha registration', sender='matcha@project.unit.ua', recipients=[email])
        message.body = "Thank tou for registration in Matcha. To activate your accont please follow the link " + request.url_root + "activate?email=" + email + '&token=' + token
        message.html = "<p>Thank tou for registration in Matcha. To activate your accont please follow the <a href= " + request.url_root + "activate?email=" + email + '&token=' + token + ">link</a></p> "
        mail.send(message)
    return json.dumps({
            'ok': True,
        })


@app.route('/activate')
def activate_account():
    email = request.args.get('email')
    token = request.args.get('token')
    status = {'activation': False, 'message': 'It does not work, sly. Invalid activation link.'}
    if email is None or token is None:
        return render_template('activation.html', status=status)
    res = user_model.check_token(email, token)
    if res:
        user_model.activate_user(res[0]['id'])
        status = {'activation': True, 'message': 'Congratulations! Your account has been successfully activated.'}
        return render_template('activation.html', status=status)
    else:
        status = {'activation': False, 'message': 'Unfortunately your account is not activated.'}
        return render_template('activation.html', status=status)



@app.route('/login', methods=['POST'])
def login():
    if 'login' in session:
        return redirect('/profile')

    email = html.escape(request.form['email'])
    password = html.escape(request.form['password'])

    if not email:
        return json.dumps({
            'ok': False,
            'error': "Please enter your email",
            'fields': ["my-email"]
        })

    if not password:
        return json.dumps({
            'ok': False,
            'error': "Please enter your password",
            'fields': ["my-password"]
        })

    user = user_model.email_exists(email)

    if user:
        if user[0]['activation'] != 1:
            return json.dumps({
                'ok': False,
                'error': "Unfortunately your account is not activated.",
            })
        password_hash = hashlib.sha3_512(password.encode('utf-8')).hexdigest()
        if user[0]['password'] == password_hash:
            session['id'] = user[0]['id']
            session['login'] = user[0]['login']
            print(session)
            return json.dumps({
                'ok': True
            })
        else:
            return json.dumps({
                'ok': False,
                'error': "Wrong password.",
                'fields': ['my-password']
            })
    else:
        return json.dumps({
            'ok': False,
            'error': "There is no user with such email.",
            'fields': ['my-email']
        })

@app.route('/newsfeed')
def newsfeed():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0]
        }
        return render_template('newsfeed.html', data=data)
    return redirect('/')


@app.route('/forgot')
def forgot():
    if 'id' in session:
        return redirect('/')
    else:
        return render_template('/forgot.html')

@app.route('/ajax_forgot', methods=["POST"])
def ajax_forgot():
    if 'id' in session:
        return redirect('/')
    else:
        email = html.escape(request.form['email'])




@app.route('/logout')
def logout():
    print(session)

    session.clear()
    return redirect(request.referrer)