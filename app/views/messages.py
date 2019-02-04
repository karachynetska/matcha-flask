from app import app, socketio
from flask import render_template, url_for, redirect, request, session
from flask_socketio import SocketIO, send
import html
import hashlib
import random
from datetime import datetime
import json
import re
from app.models import user as user_model
from flask_mail import Message

@app.route('/profile/messages')
def messages():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0]
        }
        return render_template('messages.html', data=data)
    return redirect('/')

@socketio.on("message", namespace='/profile/messages')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)
