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
from app.models import sympathys
# from app.models.friendships import check_friendship, add_friend
from flask_mail import Message
from app.settings import APP_ROOT


images = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = "app/static/media"
configure_uploads(app, images)


@app.route('/profile/photos')
def photos():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0],
            'photos': photos_model.get_photos_by_id(session.get('id'))
        }
        return render_template('photos.html', data=data)
    return redirect('/')

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
