from app import database

def search_with_geolocation(id_user):
    array = [id_user]
    sql = 'SELECT * FROM users INNER JOIN geolocation ON users.id = geolocation.id_user WHERE users.activation = 1 AND users.id != ?'
    res = database.db_query(sql, array)
    return res

def search(id_user):
    array = [id_user]
    sql = 'SELECT * FROM users WHERE id != ? AND activation = 1'
    res = database.db_query(sql, array)
    return res

def search_by_full_name(id_user, first_name, last_name):
    array = [first_name, last_name, id_user]
    sql = 'SELECT * FROM users WHERE firstname=? AND lastname=? AND id != ? AND activation = 1'
    res = database.db_query(sql, array)
    return res

def search_by_first_name(id_user, first_name):
    array = [first_name, id_user]
    sql = 'SELECT * FROM users WHERE firstname=? AND id != ? AND activation = 1'
    res = database.db_query(sql, array)
    return res

def search_by_last_name(id_user, last_name):
    array = [last_name, id_user]
    sql = 'SELECT * FROM users WHERE lastname=? AND id != ? AND activation = 1'
    res = database.db_query(sql, array)
    return res
