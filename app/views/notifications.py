from app import app, sio
from flask import render_template, url_for, redirect, request, session
import html
import hashlib
import random
from datetime import datetime
import json
import re
from flask_socketio import SocketIO, join_room, leave_room, emit, send
from app.models import user as user_model
from app.models import messages as messages_model
from app.models import notifications as notification_model
from flask_mail import Message

id_user_to_notification_sid = {}

def add_notification(to_whom_id, notification, type, image):
    notification_model.add_notification(to_whom_id, notification, type, image)
    notifications = notification_model.get_notification_by_user_id(to_whom_id)

    for key, value in id_user_to_notification_sid.items():
        if value == to_whom_id:
            emit('notification', notifications, namespace='/notifications', room=key)


@sio.on('connect', namespace='/notifications')
def connect():
    id_user_to_notification_sid[request.sid] = session.get('id')

@sio.on('disconnect', namespace='/notifications')
def disconnect():
    id_user_to_notification_sid.pop(request.sid)

