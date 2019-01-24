from app.config import database

# FRIENDS

def add_friend(id_sender, id_taker):
    status = 0
    array = [id_sender, id_taker, status]
    sql = "INSERT INTO friend_requests (id_sender, id_taker, status) VALUES (?, ?, ?)"
    res = database.db_insert(sql, array)
    return res

def delete_friend(id1, id2):
    array = [id1, id2, id2, id1]
    sql = 'DELETE FROM friendships WHERE id_user1=? AND id_user2=? OR id_user1=? AND id_user2=?'
    res = database.db_query(sql, array)
    print(res)
    return res

def check_friendship(id1, id2):
    array = [id1, id2, id2, id1]
    sql = 'SELECT * FROM friendships WHERE id_user1=? AND id_user2=? OR id_user1=? AND id_user2=?'
    res = database.db_query(sql, array)
    print(res)
    return res

def check_request(id1, id2):
    array = [id1, id2]
    sql = 'SELECT * FROM friend_requests WHERE id_sender=? AND id_taker=?'
    res = database.db_query(sql, array)
    if not res:
        array = [id2, id1]
        sql = 'SELECT * FROM friend_requests WHERE id_sender=? AND id_taker=?'
        res = database.db_query(sql, array)
        if res:
            return 'taker'
        else:
            return None
    else:
        return 'sender'

def remove_request(id1, id2):
    array = [id1, id2]
    sql = 'DELETE FROM friend_requests WHERE id_sender=? AND id_taker=?'
    res = database.db_query(sql, array)
    return res

def get_friends_list(id):
    array = [id, id]
    sql = 'SELECT * FROM friendships WHERE id_user1=? OR id_user2=?'
    res = database.db_query(sql, array)
    return res