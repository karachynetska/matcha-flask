from app.config import database

def add_notification(from_whom_id, to_whom_id, notification):
    if not check_for_notification(from_whom_id, to_whom_id, notification):
        array = [from_whom_id, to_whom_id, notification]
        sql = 'INSERT INTO notifications (from_whom_id, to_whom_id, notification) VALUES (?,?,?)'
        res = database.db_insert(sql, array)
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

def check_for_notification(from_whom_id, to_whom_id, notification):
    array = [from_whom_id, to_whom_id, notification]
    sql = 'SELECT * FROM notification WHERE from_whom_id=? AND to_whom_id=? AND notification=?'
    res = database.db_query(sql, array)
    return res