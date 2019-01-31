from app.config import database

def add_comment(id_photo, id_user, text):
    array = [id_photo, id_user, text]
    sql = 'INSERT INTO comments(id_photo, id_user, text) VALUES (?, ?, ?)'
    res = database.db_insert(sql, array)
    return res

def delete_comment(id_photo, id_user, text):
    array = [id_photo, id_user, text]
    sql = 'DELETE FROM comments WHERE id_photo=?, id_user=?, text=?'
    res = database.db_insert(sql, array)
    return res