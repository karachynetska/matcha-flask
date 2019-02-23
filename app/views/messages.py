from app import app, sio
from flask import render_template, url_for, redirect, request, session
import html
import json
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from app.models import user as user_model
from app.models import messages as messages_model
from app.views import notifications as notifications_view

id_user_to_sid = {}
id_dialogue_to_sid = {}

def check_online_status(user_id):
    print(id_user_to_sid)
    for key, value in id_user_to_sid.items():
        if value == user_id:
            return True
        else:
            return False

@app.route('/ajax_start_dialogue', methods=['POST'])
def ajax_start_dialogue():
    id_user1 = request.form['id_user1']
    id_user2 = request.form['id_user2']

    if not messages_model.check_dialogue(id_user1, id_user2):
        dialogue_name = id_user1 + id_user2
        if messages_model.create_dialogue(dialogue_name, id_user1, id_user2):
            dialogue_id = messages_model.get_dialogue_id(id_user1, id_user2)
            return json.dumps({
                'ok': True,
                'error': "The dialogue was created",
                'id_dialogue': dialogue_id
            })
    else:
        dialogue_id = messages_model.get_dialogue_id(id_user1, id_user2)
        return json.dumps({
            'ok': True,
            'error': "The exists",
            'id_dialogue': dialogue_id
        })


@app.route('/profile/messages')
def messages():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0],
            'get_user_by_id': user_model.get_user_by_id,
            'dialogues': messages_model.get_dialogues_by_user_id(session.get('id')),
            'messages': messages_model.get_messages_by_dialogue_id,
            'get_last_message_by_dialogue_id': messages_model.get_last_message_by_dialogue_id,
            'get_unread_messages_nbr': messages_model.get_unread_messages_nbr
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
    dialogue = id_dialogue_to_sid[request.sid]
    leave_room(dialogue)
    id_dialogue_to_sid.pop(request.sid)



