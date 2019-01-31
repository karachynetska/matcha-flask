from app.config import database

def like(id_photo, id_user):
    array = [id_photo, id_user]
    if check_like(id_photo, id_user):
        remove_like(id_photo, id_user)
    else:
        sql = 'INSERT INTO likes (id_photo, id_user) VALUES (?, ?)'
        res = database.db_insert(sql, array)
        if check_dislike(id_photo, id_user):
            remove_dislike(id_photo, id_user)
            return 'was'
        return res

def remove_like(id_photo, id_user):
    array = [id_photo, id_user]
    sql = 'DELETE FROM likes WHERE id_photo=? AND id_user=?'
    res = database.db_insert(sql, array)
    return res

def dislike(id_photo, id_user):
    array = [id_photo, id_user]
    if check_dislike(id_photo, id_user):
        remove_dislike(id_photo, id_user)
    else:
        sql = 'INSERT INTO dislikes (id_photo, id_user) VALUES (?, ?)'
        res = database.db_insert(sql, array)
        if check_like(id_photo, id_user):
            remove_like(id_photo, id_user)
            return 'was'
        return res

def remove_dislike(id_photo, id_user):
    array = [id_photo, id_user]
    sql = 'DELETE FROM dislikes WHERE id_photo=? AND id_user=?'
    res = database.db_insert(sql, array)
    return res

def check_like(id_photo, id_user):
    array = [id_photo, id_user]
    sql = 'SELECT * FROM likes WHERE id_photo=? AND id_user=?'
    res = database.db_query(sql, array)
    return res

def check_dislike(id_photo, id_user):
    array = [id_photo, id_user]
    sql = 'SELECT * FROM dislikes WHERE id_photo=? AND id_user=?'
    res = database.db_query(sql, array)
    return res

def photo_likes(id_photo):
    array = [id_photo]
    sql = 'SELECT * FROM likes WHERE id_photo=?'
    res = database.db_query(sql, array)
    n = len(res)
    return n

def photo_dislikes(id_photo):
    array = [id_photo]
    sql = 'SELECT * FROM dislikes WHERE id_photo=?'
    res = database.db_query(sql, array)
    n = len(res)
    return n