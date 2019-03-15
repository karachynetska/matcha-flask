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
from app.models import sympathys
from app.models import likes, comments
from app.views import notifications as notifications_view
# from app.models.friendships import check_friendship, add_friend
from flask_mail import Message
from app.settings import APP_ROOT


@app.route('/ajax_add_comment', methods=["POST"])
def ajax_add_comment():
    id_photo = request.form['id_photo']
    id_user = session.get('id')
    text = html.escape(request.form['text'])

    if not id_photo or not id_user or not text:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })
    res = comments.add_comment(id_photo, id_user, text)
    print(res)
    to_whom_id = user_model.get_user_id_by_photo_id(id_photo)
    msg = 'You have a new comment from ' + str(session.get('firstname')) + ' ' + str(session.get('lastname')) + '.'
    image = user_model.get_avatar(session.get('id'))
    notifications_view.add_notification(to_whom_id, msg, 'comment', image)
    if not res:
        return json.dumps({
            'ok': False,
            'error': "The comment has not been added"
        })
    return json.dumps({
        'ok': True,
        'error': "Commented",
        'id_comment': res
    })

@app.route('/ajax_delete_comment', methods=['POST'])
def ajax_delete_comment():
    id_comment = request.form['id_comment']
    if not id_comment:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })
    res = comments.delete_comment(id_comment)
    if res:
        return json.dumps({
            'ok': True,
            'error': "Comment deleted",
        })