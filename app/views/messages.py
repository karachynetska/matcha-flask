from app import app, sio
from flask import render_template, url_for, redirect, request, session
from flask_socketio import SocketIO, send
import html
import hashlib
import random
from datetime import datetime
import json
import re
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from app.models import user as user_model
from app.models import messages as messages_model
from flask_mail import Message

id_user_to_sid = {}
id_dialogue_to_sid = {}

@app.route('/profile/messages')
def messages():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0],
            'get_user_by_id': user_model.get_user_by_id,
            'dialogues': messages_model.get_dialogues_by_user_id(session.get('id')),
            'messages': messages_model.get_messages_by_dialogue_id,
            'get_last_message_by_dialogue_id': messages_model.get_last_message_by_dialogue_id
        }
        return render_template('messages.html', data=data)
    return redirect('/')


@sio.on('connect', namespace='/messages')
def connect():
    match = 0
    for key, value in id_user_to_sid.items():
        print(type(value))
        print(type(session.get('id')))
        if value == session.get('id'):
            match = 1
    if match == 0:
        id_user_to_sid[request.sid] = session.get('id')
    print(id_user_to_sid)

@sio.on('join_dialogue', namespace='/messages')
def join_dialogue(data):
    match = 0
    for key, value in id_dialogue_to_sid.items():
        if value == data['id_dialogue']:
            match = 1
    if match == 0:
        join_room(data['id_dialogue'])
        id_dialogue_to_sid[request.sid] = data['id_dialogue']
        messages_model.read_all_messages(data['from_whom_id'], data['to_whom_id'])

@sio.on('send_message', namespace='/messages')
def send_message(data):
    print("data")
    print(data)
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
    print("id_user_to_sid")
    print(id_user_to_sid)
    print('id_dialogue_to_sid')
    print(id_dialogue_to_sid)

    emit('add_message_to_template', data, dialogue=dialogue)

@sio.on('disconnect', namespace='/messages')
def disconnect():
    id_user_to_sid.pop(request.sid)
    print('deleted')
    print(id_user_to_sid)
    dialogue = id_dialogue_to_sid[request.sid]
    leave_room(dialogue)
    id_dialogue_to_sid.pop(request.sid)



