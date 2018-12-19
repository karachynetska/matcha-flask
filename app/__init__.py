from flask import Flask, render_template, request, redirect, url_for
from app.config import setup, database

app = Flask(__name__)

setup.initial_setup()

from app.views import auth

@app.route('/')
def index():
    return render_template('index-register.html')

