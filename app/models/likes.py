from app.config import database

def like(id_photo, id_user):
    array = [id_photo, id_user]
    if check_dislike(id_photo, id_user):
        remove_dislike(id_photo, id_user)
    sql = 'INSERT INTO likes (id_photo, id_user) VALUES (?, ?)'
    res = database.db_insert(sql, array)
    return res

def remove_like(id_photo, id_user):
    array = [id_photo, id_user]
    sql = 'DELETE FROM likes WHERE id_photo=? AND id_user=?'
    res = database.db_insert(sql, array)
    return res

def dislike(id_photo, id_user):
    array = [id_photo, id_user]
    if check_like(id_photo, id_user):
        remove_like(id_photo, id_user)
    sql = 'INSERT INTO dislikes (id_photo, id_user) VALUES (?, ?)'
    res = database.db_insert(sql, array)
    return res

def remove_dislike(id_photo, id_user):
    array = [id_photo, id_user]
    sql = 'DELETE FROM dislikes WHERE id_photo=? AND id_user=?'
    res = database.db_insert(sql, array)
    return res

def check_like(id_photo, id_user):
    array = [id_photo, id_user]
    sql = 'SELECT * FROM likes WHERE id_photo=? AND id_user=?'
    res = database.db_insert(sql, array)
    return res

def check_dislike(id_photo, id_user):
    array = [id_photo, id_user]
    sql = 'SELECT * FROM dislikes WHERE id_photo=? AND id_user=?'
    res = database.db_insert(sql, array)
    return res