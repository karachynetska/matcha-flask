from app.config import database
from datetime import datetime


def create_dialogue(dialogue_name, id_user1, id_user2):
    array = [dialogue_name, id_user1, id_user2]
    sql = "INSERT INTO dialogues (dialogue_name, id_user1, id_user2) VALUES (?, ?, ?)"
    res = database.db_insert(sql, array)
    return res

def check_dialogue(id_user1, id_user2):
    array = [id_user1, id_user2]
    sql = 'SELECT * FROM dialogues WHERE id_user1=? AND id_user2=?'
    res = database.db_query(sql, array)
    return res

def get_dialogue_id(id_user1, id_user2):
    array = [id_user1, id_user2, id_user2, id_user1]
    sql = 'SELECT id_dialogue FROM dialogues WHERE id_user1=? AND id_user2=? OR id_user1=? AND id_user2=?'
    res = database.db_query(sql, array)[0]['id_dialogue']
    return res


def send_message(id_dialogue, from_whom_id, to_whom_id, message):
    array = [id_dialogue, from_whom_id, to_whom_id, message]
    sql = 'INSERT INTO messages (id_dialogue, from_whom_id, to_whom_id, message) VALUES (?, ?, ?, ?)'
    res = database.db_insert(sql, array)
    return res


def delete_message(id_message):
    array = [id_message]
    sql = 'DELETE FROM messages WHERE id_message=?'
    res = database.db_query(sql, array)
    return res


def read_all_messages(from_whom_id, to_whom_id):
    array = [from_whom_id, to_whom_id]
    sql = 'UPDATE messages SET status="read" WHERE from_whom_id=? AND to_whom_id=?'
    res = database.db_query(sql, array)
    return res


def get_dialogues_by_user_id(id_user):
    array = [id_user, id_user]
    sql = 'SELECT * FROM dialogues WHERE id_user1=? OR id_user2=?'
    res = database.db_query(sql, array)
    return res


def get_messages_by_dialogue_id(id_dialogue):
    array = [id_dialogue]
    sql = 'SELECT * FROM messages WHERE id_dialogue=?'
    res = database.db_query(sql, array)
    return res


def get_last_message_by_dialogue_id(id_dialogue):
    array = [id_dialogue]
    sql = 'SELECT * FROM messages WHERE id_dialogue=? GROUP BY id_message ORDER BY id_message DESC LIMIT 1;'
    res = database.db_query(sql, array)
    if res:
        return res[0]['message']
    else:
        return 'There are no messages in this dialog yet'

def get_unread_messages_nbr(from_whom_id, to_whom_id):
    array = [from_whom_id, to_whom_id]
    sql = 'SELECT * FROM messages WHERE status="unread" AND from_whom_id=? AND to_whom_id=?'
    res = database.db_query(sql, array)
    n = len(res)
    return n
