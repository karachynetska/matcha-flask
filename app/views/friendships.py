from app import app, mail
from flask import render_template, url_for, redirect, request, session
from flask_uploads import configure_uploads, IMAGES, UploadSet
import html
import hashlib
import random
from datetime import datetime
import json
import re
import os
from app.models import user as user_model
from app.models import friendships
# from app.models.friendships import check_friendship, add_friend
from flask_mail import Message
from app.settings import APP_ROOT

@app.route('/ajax_add_friend')
def ajax_add_friend():
    user_id = request.args.get('user_id')
    if not friendships.check_request(session.get('id'), user_id):
        res = friendships.add_friend(session.get('id'), user_id)
        if res:
            return json.dumps({
                'ok': True,
                'error': "Friend request sent"
            })

# @app.route('/ajax_remove_request')
# def ajax_remove_request():
#     user_id = request.form('user_id')


# @app.route('/ajax_decline_request')
# def ajax_decline_request():

