from app.config import database

def add_comment(id_photo, id_user, text):
    array = [id_photo, id_user, text]
    sql = 'INSERT INTO comments(id_photo, id_user, text) VALUES (?, ?, ?)'
    res = database.db_insert(sql, array)
    return res

def delete_comment(id_comment):
    array = [id_comment]
    sql = 'DELETE FROM comments WHERE id_comment=?'
    res = database.db_insert(sql, array)
    return res

def get_comments_by_photo_id(id_photo):
    array = [id_photo]
    sql = 'SELECT * FROM comments WHERE id_photo=?'
    res = database.db_query(sql, array)
    return res