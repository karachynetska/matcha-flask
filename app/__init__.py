from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail
from app.config import setup, database
import os

app = Flask(__name__)
app.secret_key = "qnfhyamkdntiam16"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))  # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')

setup.initial_setup()

app.config.update(dict(
    MAIL_SERVER = 'smtp.googlemail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = 'unitmatcha@gmail.com',
    MAIL_PASSWORD = 'unitfactory44',
))
mail = Mail(app)

from app.views import auth, profile, messages, sympathys, photos

@app.route('/')
def index():
    if 'id' in session:
        return redirect('/profile')
    return render_template('index-register.html')

