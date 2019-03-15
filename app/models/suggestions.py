from app import database

def get_getero_or_bi_man(id_user):
    array = [id_user]
    sql = 'SELECT * FROM users WHERE id != ? AND activation = 1 AND gender = "Male" AND (sex_pref = "Heterosexual" OR sex_pref = "Bisexual")'
    res = database.db_query(sql, array)
    return res

def get_getero_or_bi_women(id_user):
    array = [id_user]
    sql = 'SELECT * FROM users WHERE id != ? AND activation = 1 AND gender = "Female" AND (sex_pref = "Heterosexual" OR sex_pref = "Bisexual")'
    res = database.db_query(sql, array)
    return res

def get_homo_or_bi_man(id_user):
    array = [id_user]
    sql = 'SELECT * FROM users WHERE id != ? AND activation = 1 AND gender = "Male" AND (sex_pref = "Homosexual" OR sex_pref = "Bisexual")'
    res = database.db_query(sql, array)
    return res

def get_homo_or_bi_women(id_user):
    array = [id_user]
    sql = 'SELECT * FROM users WHERE id != ? AND activation = 1 AND gender = "Female" AND (sex_pref = "Homosexual" OR sex_pref = "Bisexual")'
    res = database.db_query(sql, array)
    return res

def get_users_for_bi_woman(id_user):
    array = [id_user]
    sql = 'SELECT * FROM users WHERE id != ? AND activation = 1 AND (gender = "Female" AND (sex_pref = "Homosexual" OR sex_pref = "Bisexual")) OR (gender = "Male" AND (sex_pref = "Heterosexual" OR sex_pref = "Bisexual"))'
    res = database.db_query(sql, array)
    return res

def get_users_for_bi_man(id_user):
    array = [id_user]
    sql = 'SELECT * FROM users WHERE id != ? AND activation = 1 AND (gender = "Male" AND (sex_pref = "Homosexual" OR sex_pref = "Bisexual")) OR (gender = "Female" AND (sex_pref = "Heterosexual" OR sex_pref = "Bisexual"))'
    res = database.db_query(sql, array)
    return res
