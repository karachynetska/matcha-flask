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
from app.views import notifications as notification_view
from app.models import sympathys
# from app.models.friendships import check_friendship, add_friend
from flask_mail import Message
from app.settings import APP_ROOT

@app.route('/ajax_like_user')
def ajax_add_friend():
    user_id = request.args.get('user_id')
    user = user_model.get_user_by_id(session.get('id'))[0]
    if not sympathys.check_request(session.get('id'), user_id):
        res = sympathys.like_user(session.get('id'), user_id)
        if res:
            notification_view.add_notification(user_id, user['firstname'] + ' ' + user['lastname'] + ' likes you!', 'like_user')
            return json.dumps({
                'ok': True,
                'error': "Liked"
            })

@app.route('/ajax_like_back_user')
def ajax_like_back_user():
    user_id = request.args.get('user_id')
    user = user_model.get_user_by_id(session.get['id'])[0]
    if not sympathys.check_sympathy(session.get('id'), user_id):
        sympathys.like_back_user(session.get('id'), user_id)
        sympathys.add_users_to_sympathys(session.get('id'), user_id)
        notification_view.add_notification(user_id, 'You like each other! Now you can chat with ' + user['firstname'] + ' ' + user['lastname'] + '.', 'like_back_user')
        return json.dumps({
            'ok': True,
            'error': "Liked_back"
        })

@app.route('/ajax_unlike_user')
def ajax_delete_friend():
    user_id = request.args.get('user_id')
    user = user_model.get_user_by_id(session.get('id'))
    if sympathys.check_sympathy(session.get('id'), user_id):
        res = sympathys.unlike_user(session.get('id'), user_id)
        if res:
            notification_view.add_notification(user_id, user['firstname'] + ' ' + user['lastname'] + ' does not like you anymore.', 'unlike_user')
            return json.dumps({
                'ok': True,
                'error': "Unlike"
            })
# @app.route('/ajax_remove_request')
# def ajax_remove_request():
#     user_id = request.form('user_id')


# @app.route('/ajax_decline_request')
# def ajax_decline_request():

