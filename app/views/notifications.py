from app import app, sio
from flask import request, session
import json
from flask_socketio import SocketIO, emit
from app.models import notifications as notification_model
from app.models import sympathys
from datetime import datetime

id_user_to_notification_sid = {}
offline_users = {}

def get_online_users():
    online_users = []
    for key, value in id_user_to_notification_sid.items():
        if not value in online_users and value != session.get('id'):
            online_users.append(value)
    return online_users

def get_offline_users():
    offline_users_list = offline_users
    return offline_users_list


def add_notification(from_whom_id, to_whom_id, notification, type, image):
    if not sympathys.check_block(from_whom_id, to_whom_id):
        id_notification = notification_model.add_notification(to_whom_id, notification, type, image)
        notification = notification_model.get_notification_by_id(id_notification)

        tmp_dict = id_user_to_notification_sid.copy()

        for key, value in tmp_dict.items():
            if int(value) == int(to_whom_id):
                emit('notification', notification, namespace='/notifications', room=key)

@app.route('/ajax_delete_notification', methods=['POST'])
def ajax_delete_notification():
    id_notification = request.form['id_notification']
    if not id_notification:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })
    res = notification_model.delete_notification(id_notification)
    if not res:
        return json.dumps({
            'ok': True,
            'error': "Notification deleted"
        })
    else:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })

@sio.on('connect', namespace='/notifications')
def connect():
    id_user_to_notification_sid[request.sid] = session.get('id')
    if session.get('id') in offline_users:
        offline_users.pop(session.get('id'))

@sio.on('disconnect', namespace='/notifications')
def disconnect():
    if request.sid in id_user_to_notification_sid:
        id_user = id_user_to_notification_sid.get(request.sid)
        id_user_to_notification_sid.pop(request.sid)
        online_users = get_online_users()
        if not id_user in online_users:
            offline_users[id_user] = datetime.now().strftime("%d-%m-%Y %H:%M")

