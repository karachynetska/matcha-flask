from app.config import database

def user_exists(login, email):
    array = [login, email]
    sql = 'SELECT * FROM users WHERE login=? OR email=?'
    res = database.db_query(sql, array)
    return res

def save_user_to_db(login, password, firstname, lastname, email, avatar, birth_date, city, country, token, gender):
    array = [login, password, firstname, lastname, email, avatar, birth_date, city, country, token, gender]
    sql ='INSERT INTO users (login, password, firstname, lastname, email, avatar, birth_date, city, country, token, gender) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
    res = database.db_insert(sql, array)
    return res

def get_user_by_id(id):
    array= [id]
    sql = 'SELECT * FROM users WHERE id=?'
    res = database.db_query(sql, array)
    return res

