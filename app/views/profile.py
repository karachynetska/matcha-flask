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

@app.route('/profile')
def profile():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0]
        }
        return render_template('profile.html', data=data)
    return redirect('/')

@app.route('/profile/edit/password', methods=['POST', 'GET'])
def edit_password():
    if 'id' in session:
        if request.method == 'POST':
            my_password = html.escape(request.form['my_password'])
            new_password = html.escape(request.form['new_password'])
            confirm_password = html.escape(request.form['confirm_password'])
            print(my_password)

        if not my_password:
            return json.dumps({
                'ok': False,
                'error': "Enter your password please",
                'fields': ["my-password"]
            })

        if not new_password:
            return json.dumps({
                'ok': False,
                'error': "Enter your new password please",
                'fields': ["my-password"]
            })

        if not confirm_password:
            return json.dumps({
                'ok': False,
                'error': "Enter new password again please",
                'fields': ["confirm-password"]
            })

        user = user_model.get_user_by_id(session.get('id'))[0]

        my_password_hash = hashlib.sha3_512(my_password.encode('utf-8')).hexdigest()
        if my_password_hash == user.password:
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
                    'fields': ["new_password", "confirm-password"]
                })
        else:
            return json.dumps({
                'ok': False,
                'error': "You entered wrong password",
                'fields': ["my-password"]
            })

        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0]
        }
        return render_template('edit-profile-password.html', data=data)
    else:
        return redirect('/')