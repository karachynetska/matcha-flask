from app import app, mail
from flask import render_template, url_for, redirect, request, session
import html
import hashlib
import random
from datetime import datetime
import json
import re
from app.models import user as user_model
from flask_mail import Message



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

