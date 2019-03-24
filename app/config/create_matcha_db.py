import json
import string
import random
from datetime import datetime
import hashlib
import sqlite3
from sqlite3 import Error

db_name = "../../matcha.sqlite3"


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def db_query(sql, arguments=None):
    # create a database connection to a SQLite database
    try:
        conn = sqlite3.connect(db_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        if arguments:
            c.execute(sql, arguments)
        else:
            c.execute(sql)
        conn.commit()
        return c.fetchall()
    except Error as e:
        return e
    finally:
        conn.close()


def db_insert(sql, arguments=None):
    # create a database connection to a SQLite database
    try:
        conn = sqlite3.connect(db_name)
        conn.row_factory = dict_factory
        c = conn.cursor()
        if arguments:
            c.execute(sql, arguments)
        else:
            c.execute(sql)
        conn.commit()
        return c.lastrowid
    except Error as e:
        return e
    finally:
        conn.close()



def get_all_users(id):
    array = [id]
    sql = 'SELECT * FROM users WHERE id != ?'
    res = db_query(sql, array)
    return res

def save_user_to_db(login, password, firstname, lastname, email, avatar, background, birth_date, city, country, token, gender, sex_pref):
    array = [login, password, firstname, lastname, email, avatar, background, birth_date, city, country, token, gender, sex_pref]
    sql = 'INSERT INTO users (login, password, firstname, lastname, email, avatar, background, birth_date, city, country, token, gender, sex_pref) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    res = db_insert(sql, array)
    return res

def create_about_for_user(id):
    array = [id]
    sql = 'INSERT INTO about(id_user) VALUES(?)'
    res = db_insert(sql, array)
    return res

def email_exists(email):
    array = [email]
    sql = 'SELECT * FROM users WHERE email=?'
    res = db_query(sql, array)
    return res

def add_geolocation(id_user, latitude, longitude):
    array = [id_user, latitude, longitude]
    sql = 'INSERT INTO geolocation(id_user, latitude, longitude) VALUES (?, ?, ?)'
    res = db_insert(sql, array)
    return res

users = get_all_users(1)
for user in users:
    latitude = 50.4688257
    longitude = 30.4621588
    add_geolocation(user['id'], latitude, longitude)


# with open('matcha_users.json') as f:
#     data = json.load(f)
#
# gender = ['Male', 'Female']
# sex_pref = ['Heterosexual', 'Homosexual', 'Bisexual']
# email = []
#
# for user in data:
#     g = random.randint(0, 1)
#     user['gender'] = gender[g]
#
#     s = random.randint(0, 1)
#     user['sex_pref'] = sex_pref[s]
#
#     user['birth_date'] = datetime.strptime(user['birth_date'], '%m/%d/%Y')
#     password = 'blahblah42'
#     password_hash = hashlib.sha3_512(password.encode('utf-8')).hexdigest()
#
#     user['login'] = ''.join(random.choices(string.ascii_lowercase, k=5))
#     user['email'] = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
#
#
#     numb = random.randint(1, 13)
#     avatar = str(numb) + '.png'
#     avatar = '/static/avatars/' + avatar
#     background = str(numb) + '.jpg'
#     background = '/static/backgrounds/' + background
#
#     date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     token = hashlib.md5((user['login'] + date).encode('utf-8')).hexdigest()

    # print(user['login'])
    # print(password_hash)
    # print(user['firstname'])
    # print(user['lastname'])
    # print(user['email'])
    # print(avatar)
    # print(background)
    # print(user['birth_date'])
    # print(user['city'])
    # print(user['country'])
    # print(token)
    # print(user['gender'])
    # print(user['sex_pref'])
    #
    # res = save_user_to_db(user['login'], password_hash, user['firstname'], user['lastname'], user['email'], avatar, background, user['birth_date'], user['city'], user['country'], token, user['gender'], user['sex_pref'])
    # print(res)
    # if res:
    #     id_user = email_exists(user['email'])[0]['id']
    #     res = create_about_for_user(id_user)