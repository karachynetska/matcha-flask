from flask import Flask, render_template, redirect, session
from flask_socketio import SocketIO
from flask_mail import Mail
from app.config import setup, database
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = "qnfhyamkdntiam16"
# app.config['DEBUG'] = True
sio = SocketIO(app)

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

from app.views import auth, profile, messages, sympathys, photos, likes, comments, geolocation, search


@app.route('/')
def index():
    session.clear()
    if 'id' in session:
        return redirect('/profile')
    return render_template('index-register.html')


