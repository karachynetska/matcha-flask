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
from app.models import likes
# from app.models.friendships import check_friendship, add_friend
from flask_mail import Message
from app.settings import APP_ROOT

@app.route('/ajax_like', methods=['POST'])
def ajax_like():
    id_photo = request.form['id_photo']
    id_user = request.form['id_user']

    if not id_photo or not id_user:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })
    res = likes.like(id_photo, id_user)
    if res:
        if res == 'was':
            return json.dumps({
                'ok': True,
                'error': "Was dislike"
            })
        return json.dumps({
            'ok': True,
            'error': "Like"
        })
    else:
        return json.dumps({
            'ok': False,
            'error': "Remove like"
        })


@app.route('/ajax_dislike', methods=['POST'])
def ajax_dislike():
    id_photo = request.form['id_photo']
    id_user = request.form['id_user']

    if not id_photo or not id_user:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })
    res = likes.dislike(id_photo, id_user)
    if res:
        if res == 'was':
            return json.dumps({
                'ok': True,
                'error': "Was like"
            })
        return json.dumps({
            'ok': True,
            'error': "Dislike"
        })
    else:
        return json.dumps({
            'ok': False,
            'error': "Remove dislike"
        })