from app.config import database

def add_notification(to_whom_id, notification, type, image):
    array = [to_whom_id, notification, type, image]
    sql = 'INSERT INTO notifications (to_whom_id, notification, notif_type, image) VALUES (?,?,?,?)'
    res = database.db_insert(sql, array)
    return res

def get_notification_by_id(id_notification):
    array = [id_notification]
    sql = 'SELECT * FROM notifications WHERE id_notification=?'
    res = database.db_query(sql, array)
    return res

def delete_notification(id_notification):
    array = [id_notification]
    sql = 'DELETE FROM notifications WHERE id_notification=?'
    res = database.db_query(sql, array)
    return res

def get_notification_by_user_id(user_id):
    array = [user_id]
    sql = 'SELECT * FROM notifications WHERE to_whom_id=?'
    res = database.db_query(sql, array)
    return res

def delete_notifications_by_user_id(user_id):
    array = [user_id]
    sql = 'DELETE FROM notifications WHERE to_whom_id=?'
    res = database.db_query(sql, array)
    return res

def check_for_notification(to_whom_id, notification):
    array = [to_whom_id, notification]
    sql = 'SELECT * FROM notifications WHERE to_whom_id=? AND notification=?'
    res = database.db_query(sql, array)
    return res