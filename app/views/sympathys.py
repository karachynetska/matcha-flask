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
def ajax_like_user():
    user_id = request.args.get('user_id')
    check = sympathys.check_request(session.get('id'), user_id)
    print(check)
    if not check:
        res = sympathys.like_user(session.get('id'), user_id)
        if res:
            msg = str(session.get('firstname')) + ' ' + str(session.get('lastname')) + ' likes you!'
            image = user_model.get_avatar(session.get('id'))
            notification_view.add_notification(user_id, msg, 'like_user', image)
            return json.dumps({
                'ok': True,
                'error': "Liked"
            })
        else:
            return json.dumps({
                'ok': False,
                'error': "Something went wrong"
            })
    else:
        return json.dumps({
            'ok': False,
            'error': "It's your friend"
        })

@app.route('/ajax_pick_up_like')
def ajax_pick_up_like():
    user_id = request.args.get('user_id')
    if not sympathys.check_sympathy(session.get('id'), user_id):
        print('blah')
        if sympathys.check_request(session.get('id'), user_id) == 'sender':
            print('blah1')
            if sympathys.check_request_status(session.get('id'), user_id)[0]['status'] == 0:
                print('blah2')
                if sympathys.remove_request(session.get('id'), user_id) == []:
                    print('blah3')
                    return json.dumps({
                        'ok': True,
                        'error': "Pick_up_like"
                    })
                else:
                    return json.dumps({
                        'ok': False,
                        'error': "Something went wrong."
                    })
    else:
        return json.dumps({
            'ok': False,
            'error': "It's your friend"
        })

@app.route('/ajax_like_back_user')
def ajax_like_back_user():
    user_id = request.args.get('user_id')
    if not sympathys.check_sympathy(session.get('id'), user_id):
        sympathys.like_back_user(session.get('id'), user_id)
        sympathys.add_users_to_sympathys(session.get('id'), user_id)

        msg = 'You like each other! Now you can chat with ' + str(session.get('firstname')) + ' ' + str(session.get('lastname')) + '.'
        image = user_model.get_avatar(session.get('id'))
        notification_view.add_notification(user_id, msg, 'like_back_user', image)
        return json.dumps({
            'ok': True,
            'error': "Liked_back"
        })

@app.route('/ajax_unlike_user')
def ajax_delete_friend():
    user_id = request.args.get('user_id')
    if sympathys.check_sympathy(session.get('id'), user_id):
        print('blah')
        if sympathys.check_request(session.get('id'), user_id) == 'sender':
            print('blah1')
            sympathys.remove_request(session.get('id'), user_id)
        else:
            print('blah2')
            sympathys.set_request_status_to_zero(session.get('id'), user_id)
        if sympathys.unlike_user(session.get('id'), user_id):
            print('blah3')
            msg = str(session.get('firstname')) + ' ' + str(session.get('lastname')) + ' does not like you anymore.'
            image = user_model.get_avatar(session.get('id'))
            notification_view.add_notification(user_id, msg, 'unlike_user', image)
            return json.dumps({
                'ok': True,
                'error': "Unlike"
            })
# @app.route('/ajax_remove_request')
# def ajax_remove_request():
#     user_id = request.form('user_id')


# @app.route('/ajax_decline_request')
# def ajax_decline_request():

