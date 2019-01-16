from app.config import database
from datetime import datetime
import hashlib

def user_exists(login, email):
    array = [login, email]
    sql = 'SELECT * FROM users WHERE login=? OR email=?'
    res = database.db_query(sql, array)
    return res

def login_exists(login):
    array = [login]
    sql = 'SELECT * FROM users WHERE login=?'
    res = database.db_query(sql, array)
    return res

def email_exists(email):
    array = [email]
    sql = 'SELECT * FROM users WHERE email=?'
    res = database.db_query(sql, array)
    return res


def save_user_to_db(login, password, firstname, lastname, email, avatar, background, birth_date, city, country, token, gender, sex_pref):
    array = [login, password, firstname, lastname, email, avatar, background, birth_date, city, country, token, gender, sex_pref]
    sql = 'INSERT INTO users (login, password, firstname, lastname, email, avatar, background, birth_date, city, country, token, gender, sex_pref) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    res = database.db_insert(sql, array)
    return res


def get_user_by_id(id):
    array = [id]
    sql = 'SELECT * FROM users WHERE id=?'
    res = database.db_query(sql, array)
    return res

def create_token(id, login):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    token = hashlib.md5((login + date).encode('utf-8')).hexdigest()
    array = [token, id, login]
    sql = 'UPDATE users SET token=? WHERE id=? AND login=?'
    database.db_query(sql, array)
    return token

def check_token(email, token):
    array = [email]
    sql = 'SELECT id, token, activation FROM users WHERE email=?'
    res = database.db_query(sql, array)
    if not res:
        return False
    if res[0]['token'] == token:
        print(res)
        return res
    else:
        return False

def activate_user(id):
    array = [id]
    sql = 'UPDATE users SET activation = 1, token = NULL WHERE id=?'
    res = database.db_query(sql, array)
    return res

def get_avatar(id):
    array = [id]
    sql = 'SELECT avatar FROM users WHERE id=?'
    res = database.db_query(sql, array)
    return res

def recovery_password(id, password):
    array = [password, id]
    sql = 'UPDATE users SET password=?, token = NULL WHERE id=?'
    res = database.db_insert(sql, array)
    return res

#EDIT PROFILE
def change_avatar(avatar, id):
    array = [avatar, id]
    sql = 'UPDATE USERS SET avatar=? WHERE id=?'
    res = database.db_query(sql, array)
    return res

def change_password(id, password):
    array = [password, id]
    sql = 'UPDATE users SET password=? WHERE id=?'
    res = database.db_query(sql, array)
    return res

def change_firstname(firstname, id):
    array = [firstname, id]
    sql = 'UPDATE users SET firstname=? WHERE id=?'
    res = database.db_query(sql, array)
    return res

def change_lastname(lastname, id):
    array = [lastname, id]
    sql = 'UPDATE users SET lastname=? WHERE id=?'
    res = database.db_query(sql, array)
    return res

def change_email(email, id):
    array = [email, id]
    sql = 'UPDATE users SET email=? WHERE id=?'
    res = database.db_query(sql, array)
    return res

def change_birth_date(birth_date, id):
    array = [birth_date, id]
    sql = 'UPDATE users SET birth_date=? WHERE id=?'
    res = database.db_query(sql, array)
    return res

def change_gender(gender, id):
    array = [gender, id]
    sql = 'UPDATE users SET gender=? WHERE id=?'
    res = database.db_query(sql, array)
    return res

def change_sex_pref(sex_pref, id):
    array = [sex_pref, id]
    sql = 'UPDATE users SET sex_pref=? WHERE id=?'
    res = database.db_query(sql, array)
    return res

def change_city(city, id):
    array = [city, id]
    sql = 'UPDATE users SET city=? WHERE id=?'
    res = database.db_query(sql, array)
    return res

def change_country(country, id):
    array = [country, id]
    sql = 'UPDATE users SET country=? WHERE id=?'
    res = database.db_query(sql, array)
    return res

def change_my_info(my_info, id):
    array = [my_info, id]
    sql = 'UPDATE users SET my_info=? WHERE id=?'
    res = database.db_query(sql, array)
    return res