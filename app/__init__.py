from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail
from app.config import setup, database

app = Flask(__name__)

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

from app.views import auth

@app.route('/')
def index():
    return render_template('index-register.html')

