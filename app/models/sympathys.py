from app.config import database

# FRIENDS

def like_user(id_sender, id_taker):
    status = 0
    array = [id_sender, id_taker, status]
    sql = "INSERT INTO requests (id_sender, id_taker, status) VALUES (?, ?, ?)"
    res = database.db_insert(sql, array)
    return res

def like_back_user(id_sender, id_taker):
    array = [id_sender, id_taker, id_taker, id_sender]
    sql = 'UPDATE requests SET status=1 WHERE id_sender=? AND id_taker=? OR id_sender=? AND id_taker=?'
    res = database.db_insert(sql, array)
    return res

def add_users_to_sympathys(id_user1, id_user2):
    array = [id_user1, id_user2]
    sql = 'INSERT INTO sympathys (id_user1, id_user2) VALUES (?,?)'
    res = database.db_insert(sql, array)
    return res

def unlike_user(id1, id2):
    array = [id1, id2, id2, id1]
    sql = 'DELETE FROM sympathys WHERE id_user1=? AND id_user2=? OR id_user1=? AND id_user2=?'
    res = database.db_query(sql, array)
    print(res)
    return res

def check_sympathy(id1, id2):
    array = [id1, id2, id2, id1]
    sql = 'SELECT * FROM sympathys WHERE id_user1=? AND id_user2=? OR id_user1=? AND id_user2=?'
    res = database.db_query(sql, array)
    return res

def check_request(id1, id2):
    array = [id1, id2]
    sql = 'SELECT * FROM requests WHERE id_sender=? AND id_taker=?'
    res = database.db_query(sql, array)
    if not res:
        array = [id2, id1]
        sql = 'SELECT * FROM requests WHERE id_sender=? AND id_taker=?'
        res = database.db_query(sql, array)
        if res:
            return 'taker'
        else:
            return None
    else:
        return 'sender'

def remove_request(id1, id2):
    array = [id1, id2]
    sql = 'DELETE FROM requests WHERE id_sender=? AND id_taker=?'
    res = database.db_query(sql, array)
    return res

def get_sympathys_list(id):
    array = [id, id]
    sql = 'SELECT * FROM sympathys WHERE id_user1=? OR id_user2=?'
    res = database.db_query(sql, array)
    return res
