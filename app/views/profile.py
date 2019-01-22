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
from app.models.friendships import check_friendship, add_friend
from flask_mail import Message
from app.settings import APP_ROOT

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = "app/static/media"
configure_uploads(app, photos)

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = set(['image/jpg', 'image/jpeg', 'image/JPG', 'image/JPEG', 'image/png', 'image/PNG', 'image/gif', 'image/GIF'])

def allowed_extensions(mime_type):
    return mime_type in ALLOWED_EXTENSIONS



# PROFILE
@app.route('/profile')
@app.route('/profile/id<int:id_user>/')
def profile(id_user=None):
    if not 'id' in session and not id_user:
        return redirect('/')
    if 'id' in session:
        user = user_model.get_user_by_id(session.get('id'))[0]

    if id_user:
        user = user_model.get_user_by_id(id_user)[0]
    data = {
        'user': user,
        'check_friendship': check_friendship

    }
    return render_template('profile.html', data=data)




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


@app.route('/ajax_edit_basic', methods=['POST'])
def ajax_edit_basic():
    firstname = html.escape(request.form['firstname'])
    lastname = html.escape(request.form['lastname'])
    email = html.escape(request.form['email'])
    day = request.form['day']
    month = request.form['month']
    year = request.form['year']
    gender = request.form['gender']
    sex_pref = request.form['sex_pref']
    city = request.form['city']
    country = request.form['country']
    my_info = html.escape(request.form['my_info'])

    id = session.get('id')
    if firstname:
        if (len(firstname) < 2) or (len(firstname) > 25):
            return json.dumps({
                'ok': False,
                'error': "Firstname length must be from 2 characters to 25",
                'fields': ["firstname"]
            })
        user_model.change_firstname(firstname, id)
        return json.dumps({
            'ok': True,
            'error': "Changes successfully changed"
        })

    if lastname:
        if (len(lastname) < 2) or (len(lastname) > 25):
            return json.dumps({
                'ok': False,
                'error': "Lastname length must be from 2 characters to 25",
                'fields': ["lastname"]
            })
        user_model.change_lastname(lastname, id)
        return json.dumps({
            'ok': True,
            'error': "Changes successfully changed"
        })

    if email:
        if not re.match("^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$", email.lower()):
            return json.dumps({
                'ok': False,
                'error': "Wrong email",
                'fields': ["email"]
            })
        user_model.change_email(email, id)
        return json.dumps({
            'ok': True,
            'error': "Changes successfully changed"
        })

    if day and month and year:
        birth_date = request.form['day'] + '/' + request.form['month'] + '/' + request.form['year']
        try:
            birth_date = datetime.strptime(birth_date, '%d/%b/%Y')
        except:
            return json.dumps({
                'ok': False,
                'error': "Wrong date",
                'fields': ["day", "month", "year"]
            })
        user_model.change_birth_date(birth_date, id)
        return json.dumps({
            'ok': True,
            'error': "Changes successfully changed"
        })

    if gender:
        user_model.change_gender(gender, id)
        return json.dumps({
            'ok': True,
            'error': "Changes successfully changed"
        })

    if sex_pref:
        user_model.change_sex_pref(sex_pref, id)
        return json.dumps({
            'ok': True,
            'error': "Changes successfully changed"
        })

    if city:
        user_model.change_city(city, id)
        return json.dumps({
            'ok': True,
            'error': "Changes successfully changed"
        })

    if country:
        user_model.change_country(country, id)
        return json.dumps({
            'ok': True,
            'error': "Changes successfully changed"
        })



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
            'user': user_model.get_user_by_id(session.get('id'))[0],
            'interests': user_model.get_interests_by_user_id(session.get('id'))
        }
        return render_template('edit-profile-interests.html', data=data)
    else:
        return redirect('/')


@app.route('/ajax_edit_interests', methods=['POST'])
def ajax_edit_interests():
    interest = html.escape(request.form['interest'])
    icon = None

    if not interest:
        return json.dumps({
            'ok': False,
            'error': "Enter your interest please",
            'fields': ["interest"]
        })

    icon_array = {
        'fas fa-gamepad': ['game', 'games', 'playstation', 'xbox', 'игры', 'плойка'],
        'fas fa tree': ['nature', 'природа'],
        'fas fa-car': ['car', 'cars', 'race', 'racing', 'машины', 'тачки', 'гонки'],
        'fas fa-motorcycle': ['motorcycle', 'motorcycles', 'мотоцикл', 'мотоциклы'],
        'fas fa-bicycle': ['bicycle', 'bicycles', 'cycling', 'велосипед', 'велосипеды', 'велопрогулки', 'велопрогулка'],
        'fas fa-tv': ['tv', 'television', 'телевизор', 'телевидение'],
        'fas fa-paw': ['pets', 'animals', 'pet', 'animal', 'животное', 'животные', 'звери'],
        'fas fa-cat': ['cat', 'cats', 'pussycat', 'pussycats', 'кошка', 'кошки', 'кот', 'коты', 'котики', 'котяры'],
        'fas fa-dog': ['dog', 'dogs', 'doggy', 'doggies', 'собака', 'собаки', 'пес', 'псы', 'собачки', 'песики', 'собачка'],
        'fas fa-music': ['music', 'pop', 'rock', 'rap', 'jazz', 'hip-hop', 'classical music', 'singing', 'sing', 'музыка', 'рэп', 'джаз', 'поп', 'рок', 'классическая музыка', 'хип-хоп', 'пение'],
        'fas fa-guitar': ['guitar', 'guitars', 'гитара', 'гитары'],
        'fas fa-camera-retro': ['camera', 'photo', 'photos', 'taking photo', 'taking photos', 'photography', 'фото', 'фотки', 'фотосъемка'],
        'fab fa-apple': ['apple', 'ios', 'iphone', 'айфон', 'айфоны', 'эпл'],
        'fas fa-bed': ['bed', 'sleep', 'sleeping', 'спать', 'сон'],
        'fas fa-bowling-ball': ['bowling', 'боулинг'],
        'fas fa-wine-glass': ['wine', 'vodka', 'whiskey', 'bourbon', 'beer', 'alcohol', 'cocktailes', 'cocktaile', 'вино', 'винишко', 'водка', 'пиво', 'виски', 'бурбон', 'коньяк', 'алкоголь', 'выпивка'],
        'fas fa-terminal': ['code', 'coding', 'programming', 'программирование', 'код', 'кодинг', 'c', 'c++', 'c#'],
        'fab fa-python': ['python', 'питон', 'пайтон'],
        'fas fa-swimmer': ['swimming', 'pool', 'swimming pool', 'swim', 'плавание', 'бассейн'],
        'fab fa-js': ['js', 'javascript'],
        'fab fa-node-js': ['node js', 'node', 'node.js'],
        'fas fa-book-reader': ['book', 'books', 'reading', 'read', 'чтение', 'книга', 'книги', 'книжки'],
        'fas fa-plane': ['travel', 'traveling', 'airplane', 'airplanes', 'aircraft', 'путешествие', 'путешествия', 'самолеты', 'самолет', 'полет'],
        'fas fa-utensils': ['eating', 'food', 'meal', 'restaurants', 'restaurant', 'cafe', 'еда', 'есть', 'кафе', 'ресторан', 'рестораны'],
        'fas fa-smoking': ['smoke', 'smoking', 'cigarettes', 'cigarette', 'курение', 'сигарета', 'сигара', 'сигары', 'сигареты', 'папиросы', 'папироса'],
        'fas fa-skiing': ['ski', 'skiing', 'лыжи', 'лыжный спорт', 'кататься на лыжах'],
        'fas fa-snowboarding': ['snowboard', 'snowboarding', 'сноуборд', 'кататься на сноуборде', 'катание на сноуборде'],
        'fas fa-film': ['film', 'films', 'cinema', 'movie', 'movies', 'cartoon', 'cartoons', 'кино', 'кинотеатр', 'фильм', 'фильмы', 'мультики', 'мультик']
    }
    for key, value in icon_array.items():
        if interest.lower() in value:
            icon = key
    res = user_model.add_interest(interest, icon, session.get('id'))
    if res:
        return json.dumps({
            'ok': True,
            'error': "Interest successfully added"
        })

#
# @app.route('/ajax_delete_interest', methods=['POST'])
# def ajax_delete_interest():



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

    if not avatar:
        return json.dumps({
            'ok': False,
            'error': "Something wrong",
            'fields': ["avatar"]
        })
    id = session.get('id')
    login = session.get('login')
    user = user_model.get_user_by_id(id)[0]

    extension = avatar.filename.rsplit('.', 1)[1]
    avatar_name = str('avatar' + '_' + login + '.' + extension)
    path = '/static/media/' + login + '/' + avatar_name

    # CHECK IF AVATAR LOADED EARLIER EXISTS
    avatar_extension = user['avatar'].rsplit('.', 1)[1]
    name = (APP_ROOT + '/static/media/' + login + '/avatar_' + login + '.' + avatar_extension).strip()

    # DELETE IF EXISTS
    if os.path.isfile(name):
        os.remove(name)

    # SAVE AVATAR TO FOLDER
    photos.save(avatar, login, avatar_name)

    # CHANGE AVATAR IN DB
    user_model.change_avatar(path, id)
    return json.dumps({
        'ok': True,
        'error': "Avatar successfully uploaded",
    })
