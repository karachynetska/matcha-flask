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
from flask_mail import Message
from app.settings import APP_ROOT

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = "app/static/media"
configure_uploads(app, photos)

ALLOWED_EXTENSIONS = set(['image/jpg', 'image/jpeg', 'image/JPG', 'image/JPEG', 'image/png', 'image/PNG', 'image/gif', 'image/GIF'])

def allowed_extensions(mime_type):
	return mime_type in ALLOWED_EXTENSIONS

# PROFILE
@app.route('/profile')
def profile():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0]
        }
        return render_template('profile.html', data=data)
    return redirect('/')



# ABOUT
@app.route('/profile/about')
def about():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0]
        }
        return render_template('about.html', data=data)
    return redirect('/')



# FRIENDS
@app.route('/profile/friends')
def friends():
    data = {
        'user': user_model.get_user_by_id(session.get('id'))[0]
    }
    return render_template('friends.html', data=data)



# ALBUM
@app.route('/profile/album')
def album():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0]
        }
        return render_template('album.html', data=data)
    return redirect('/')



# EDIT BASIC INFORMATION
@app.route('/profile/edit/basic')
def edit_basic():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0]
        }
        return render_template('edit-profile-basic.html', data=data)
    else:
        return redirect('/')


# @app.route('/ajax_edit_basic')
# def ajax_edit_basic():
#


# EDIT PASSWORD
@app.route('/profile/edit/password')
def edit_password():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0]
        }
        return render_template('edit-profile-password.html', data=data)
    else:
        return redirect('/')


@app.route('/ajax_edit_password', methods=["POST"])
def ajax_edit_password():
    if 'id' in session:
        my_password = html.escape(request.form['my_password'])
        new_password = html.escape(request.form['new_password'])
        confirm_password = html.escape(request.form['confirm_password'])
        if not my_password:
            return json.dumps({
                'ok': False,
                'error': "Enter your password please",
                'fields': ["my_password"]
            })

        if not new_password:
            return json.dumps({
                'ok': False,
                'error': "Enter your new password please",
                'fields': ["my_password"]
            })

        if not confirm_password:
            return json.dumps({
                'ok': False,
                'error': "Enter new password again please",
                'fields': ["confirm_password"]
            })

        user = user_model.get_user_by_id(session.get('id'))[0]
        my_password_hash = hashlib.sha3_512(my_password.encode('utf-8')).hexdigest()
        if my_password_hash == user['password']:
            if new_password == confirm_password:
                if len(new_password) < 2 or len(new_password) > 25:
                    return json.dumps({
                        'ok': False,
                        'error': "Password length must be from 8 characters to 16",
                        'fields': ["new_password"]
                    })

                if re.search("[a-zA-Z]+", new_password) is None or re.search("[0-9]+", new_password) is None:
                    return json.dumps({
                        'ok': False,
                        'error': "Password is too weak",
                        'fields': ["new_password"]
                    })
                new_password_hash = hashlib.sha3_512(new_password.encode('utf-8')).hexdigest()
                user_model.change_password(session.get('id'), new_password_hash)
                return json.dumps({
                    'ok': True,
                    'error': "Your password successfully changed"
                })
            else:
                return json.dumps({
                    'ok': False,
                    'error': "Passwords don't match",
                    'fields': ["new_password", "confirm_password"]
                })
        else:
            return json.dumps({
                'ok': False,
                'error': "You entered wrong password",
                'fields': ["my_password"]
            })
    else:
        return redirect('/')



# EDIT INTERESTS
@app.route('/profile/edit/interests')
def edit_interests():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0]
        }
        return render_template('edit-profile-interests.html', data=data)
    else:
        return redirect('/')


# @app.route('/ajax_edit_interests')
# def ajax_edit_interests():



# EDIT EDUCATION AND WORK
@app.route('/profile/edit/edu-work')
def edit_edu_work():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0]
        }
        return render_template('edit-profile-edu-work.html', data=data)
    else:
        return redirect('/')


# @app.route('/ajax_edit_edu_work')
# def ajax_edit_edu_work():



# EDIT ACCOUNT SETTINGS
@app.route('/profile/edit/settings')
def edit_settings():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0]
        }
        return render_template('edit-profile-settings.html', data=data)
    else:
        return redirect('/')



#CHANGE AVATAR
@app.route('/profile/edit/avatar')
def edit_avatar():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0]
        }
        return render_template('edit-profile-avatar.html', data=data)
    else:
        return redirect('/')


@app.route('/ajax_edit_avatar', methods=['POST'])
def ajax_edit_avatar():
    avatar = request.files.get('avatar')
    print(avatar)
    if not avatar:
        return json.dumps({
            'ok': False,
            'error': "Something wrong",
            'fields': ["avatar"]
        })

    MAX_FILE_SIZE = 1024 * 1024 + 1
    if bool(avatar.filename):
        avatar_bytes = avatar.read(MAX_FILE_SIZE)
        if avatar_bytes == MAX_FILE_SIZE:
            return json.dumps({
                'ok': False,
                'error': "Image size too large",
                'fields': ["avatar"]
            })
        res = allowed_extensions(avatar.content_type)
        if res:
            id = session.get('id')
            login = session.get('login')
            user = user_model.get_user_by_id(id)[0]
            extension = avatar.filename.rsplit('.', 1)[1]
            avatar_name = str('avatar' + '_' + login + '.' + extension)
            path = '/static/media/' + login + '/' + avatar_name
            avatar_extension = user['avatar'].rsplit('.', 1)[1]
            name = (APP_ROOT + '/static/media/' + login + '/avatar_' + login + '.' + avatar_extension).strip()

            if os.path.isfile(name):
                os.remove(name)
            photos.save(avatar, login, avatar_name)

            user_model.change_avatar(path, id)
            return json.dumps({
                'ok': True,
                'error': "Image successfully uploaded",
                'path': ""
            })
        else:
            return json.dumps({
                'ok': False,
                'error': "Allowed to download files of the following formats: jpg, jpeg, png, gif",
                'fields': ["avatar"]
            })
