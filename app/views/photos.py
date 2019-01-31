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
from app.models import photos as photos_model
from app.models import likes
from app.models import sympathys
# from app.models.friendships import check_friendship, add_friend
from flask_mail import Message
from app.settings import APP_ROOT


images = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = "app/static/media"
configure_uploads(app, images)


@app.route('/profile/photos')
@app.route('/profile/photos/id<int:id_user>/')
def photos(id_user=None):
    if not 'id' in session and not id_user:
        return redirect('/')
    if 'id' in session:
        id = session.get('id')
        user = user_model.get_user_by_id(id)[0]
        photos = photos_model.get_photos_by_id(id)

    if id_user:
        user = user_model.get_user_by_id(id_user)[0]
        photos = photos_model.get_photos_by_id(id_user)

    data = {
        'user': user,
        'photos': photos,
        'get_user_by_id': user_model.get_user_by_id,
        'likes': likes.photo_likes,
        'dislikes': likes.photo_dislikes,
        'check_like': likes.check_like,
        'check_dislike': likes.check_dislike
    }
    return render_template('photos.html', data=data)


@app.route('/ajax_add_photo', methods=["POST"])
def ajax_add_photo():
    photo = request.files.get('photo')

    if not photo:
        return json.dumps({
            'ok': False,
            'error': "Something wrong"
        })

    login = session.get('login')

    extension = photo.filename.rsplit('.', 1)[1]
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    photo_name = str(login + date + '.' + extension)
    path = '/static/media/' + login + '/' + photo_name
    images.save(photo, login, photo_name)
    photos_model.add_photo(session.get('id'), path)
    return json.dumps({
        'ok': True,
        'error': "Photo successfully uploaded"
    })