from app.config import database

# FRIENDS

def add_friend(id_sender, id_taker):
    status = 0
    array = [id_sender, id_taker, status]
    sql = "INSERT INTO friend_requests (id_sender, id_taker, status) VALUES (?, ?, ?)"
    res = database.db_insert(sql, array)
    return res

def check_friendship(id1, id2):
    array = [id1, id2]
    sql = 'SELECT * FROM friendships WHERE id_user1=? AND id_user2=?'
    res = database.db_query(sql, array)
    print(res)
    return res