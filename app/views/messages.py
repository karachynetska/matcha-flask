from app import app, sio
from flask import render_template, url_for, redirect, request, session
import html
import json
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from app.models import user as user_model
from app.models import messages as messages_model
from app.views import notifications as notifications_view
from app.models import sympathys as sympathys_model

id_user_to_sid = {}
id_dialogue_to_sid = {}

def check_online_status(user_id):
    print(id_user_to_sid)
    for key, value in id_user_to_sid.items():
        if value == user_id:
            return True
        else:
            return False

@app.route('/profile/messages')
@app.route('/profile/messages/dialogue_with_<int:with_id>')
def messages(with_id=None):
    if 'id' in session:
        dialogue_id = None
        if with_id:
            my_id = session.get('id')
            if sympathys_model.check_sympathy(my_id, with_id):
                if not messages_model.check_dialogue(my_id, with_id):
                    dialogue_name = my_id + with_id
                    if messages_model.create_dialogue(dialogue_name, my_id, with_id):
                        dialogue_id = messages_model.get_dialogue_id(my_id, with_id)
                else:
                    dialogue_id = messages_model.get_dialogue_id(my_id, with_id)
            else:
                redirect('/profile/id'+with_id)
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0],
            'get_user_by_id': user_model.get_user_by_id,
            'dialogues': messages_model.get_dialogues_by_user_id(session.get('id')),
            'messages': messages_model.get_messages_by_dialogue_id,
            'get_last_message_by_dialogue_id': messages_model.get_last_message_by_dialogue_id,
            'get_unread_messages_nbr': messages_model.get_unread_messages_nbr,
            'unread_messages_nbr': messages_model.get_unread_messages_nbr_by_user_id(session.get('id')),
            'dialogue_id': dialogue_id
        }
        return render_template('messages.html', data=data)
    return redirect('/')


@sio.on('connect', namespace='/messages')
def connect():
    id_user_to_sid[request.sid] = session.get('id')

@sio.on('join_dialogue', namespace='/messages')
def join_dialogue(data):
    join_room(data['id_dialogue'])
    id_dialogue_to_sid[request.sid] = data['id_dialogue']
    messages_model.read_all_messages(data['to_whom_id'], data['from_whom_id'])

@sio.on('send_message', namespace='/messages')
def send_message(data):
    dialogue = id_dialogue_to_sid[request.sid]
    from_whom_id = data['from_whom_id']
    to_whom_id = data['to_whom_id']
    message = html.escape(data['message'])
    data['message'] = message
    user = user_model.get_user_by_id(from_whom_id)[0]
    data['user'] = user
    data['dialogue'] = dialogue
    data['last_message'] = messages_model.get_last_message_by_dialogue_id(dialogue)
    messages_model.send_message(dialogue, from_whom_id, to_whom_id, message)
    emit('add_message_to_template', data, room=dialogue)
    if not check_online_status(to_whom_id):
        notifications_view.add_notification(to_whom_id, 'You have a new message from '+ user['firstname'] + ' ' + user['lastname'], 'message', user['avatar'])

@sio.on('disconnect', namespace='/messages')
def disconnect():
    id_user_to_sid.pop(request.sid)
    # dialogue = id_dialogue_to_sid[request.sid]
    dialogue = id_dialogue_to_sid.get(request.sid)
    leave_room(dialogue)
    id_dialogue_to_sid.pop(request.sid)



