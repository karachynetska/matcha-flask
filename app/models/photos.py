from app.config import database
from datetime import datetime

def get_photos_by_id(id_user):
    array = [id_user]
    sql = 'SELECT * FROM photos WHERE id_user=?'
    res = database.db_query(sql, array)
    return res

def get_photos_nbr_by_id(id_user):
    array = [id_user]
    sql = 'SELECT * FROM photos WHERE id_user=?'
    res = database.db_query(sql, array)
    return len(res)

def add_photo(id_user, photo):
    array = [id_user, photo]
    sql = 'INSERT INTO photos (id_user, photo) VALUES (?, ?)'
    res = database.db_insert(sql, array)
    return res

def delete_photo_by_id(id_photo):
    array = [id_photo]
    sql = 'DELETE FROM photos WHERE id_photo=?'
    res = database.db_query(sql, array)
    return res

