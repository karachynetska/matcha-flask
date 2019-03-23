from app.config import database

def add_geolocation(id_user, latitude, longitude):
    array = [id_user, latitude, longitude]
    sql = 'INSERT INTO geolocation(id_user, latitude, longitude) VALUES (?, ?, ?)'
    res = database.db_insert(sql, array)
    return res

def change_geolocation(id_user, latitude, longitude):
    array = [latitude, longitude, id_user]
    sql = 'UPDATE geolocation SET latitude=?, longitude=? WHERE id_user=?'
    res = database.db_query(sql, array)
    return res

def get_geolocation_by_user_id(id_user):
    array = [id_user]
    sql = 'SELECT * FROM geolocation WHERE id_user=?'
    res = database.db_query(sql, array)
    if res:
        return res[0]
    else:
        return False

