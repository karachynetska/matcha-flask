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
# from app.models.friendships import check_friendship, add_friend
from flask_mail import Message
from app.settings import APP_ROOT


@app.route('/ajax_add_comment', methods=["POST"])
def ajax_add_comment():
    id_photo = request.form['id_photo']
    id_user = session.get('id')
    text = html.escape(request.form['text'])

    if not id_photo or not id_user or not text:
        print('not')
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })
    res = comments.add_comment(id_photo, id_user, text)
    print(res)
    if not res:
        print('faaalse')
        return json.dumps({
            'ok': False,
            'error': "The comment has not been added"
        })
    return json.dumps({
        'ok': True,
        'error': "Commented"
    })

