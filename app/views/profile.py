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

@app.route('/profile/edit/password')
def edit_password():
    if 'id' in session:
        return render_template('edit-profile-password.html')
    return redirect('/')