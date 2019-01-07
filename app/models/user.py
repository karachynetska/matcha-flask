from app.config import database


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


def save_user_to_db(login, password, firstname, lastname, email, background, avatar, birth_date, city, country, token, gender):
    array = [login, password, firstname, lastname, email, avatar, background, birth_date, city, country, token, gender]
    sql = 'INSERT INTO users (login, password, firstname, lastname, email, avatar, background, birth_date, city, country, token, gender) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    res = database.db_insert(sql, array)
    return res


def get_user_by_id(id):
    array = [id]
    sql = 'SELECT * FROM users WHERE id=?'
    res = database.db_query(sql, array)
    return res

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



