from app import database

def get_suggestion(id_user, gender, sex_pref):
    array = [id_user, id_user, id_user, gender, sex_pref]
    sql = 'SELECT * FROM users INNER JOIN requests r ON users.id = r.id_sender AND r.id_sender != ?  AND r.id_taker != ?  WHERE users.id != ? AND users.activation = 1 AND users.gender = ? AND users.sex_pref = ?'
    res = database.db_query(sql, array)
    return res

def get_getero_or_bi_user(id_user, gender):
    array = [id_user, gender]
    sql = 'SELECT * FROM users WHERE id != ? AND activation = 1 AND gender = ? AND sex_pref = "Heterosexual" OR sex_pref = "Bisexual"'
    res = database.db_query(sql, array)
    print(res)
    return res