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

