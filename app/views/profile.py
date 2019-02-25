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
from app.views import notifications as notification_view
from app.models import sympathys
# from app.models.friendships import check_friendship, add_friend
from flask_mail import Message
from app.settings import APP_ROOT

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = "app/static/media"
configure_uploads(app, photos)



# PROFILE
@app.route('/profile')
@app.route('/profile/id<int:id_user>/')
def profile(id_user=None):
    if not 'id' in session and not id_user:
        return redirect('/')
    if 'id' in session:
        user = user_model.get_user_by_id(session.get('id'))[0]
        friends = sympathys.get_sympathys_list(session.get('id'))

    if id_user:
        user = user_model.get_user_by_id(id_user)[0]
        friends = sympathys.get_sympathys_list(id_user)
        msg = str(session.get('firstname')) + ' ' + str(session.get('lastname')) + ' viewed your profile.'
        image = user_model.get_avatar(session.get('id'))
        notification_view.add_notification(id_user, msg,'view', image)
    data = {
        'user': user,
        'sympathys': sympathys,
        'friends': friends
    }
    return render_template('profile.html', data=data)




# ABOUT
@app.route('/profile/about')
@app.route('/profile/about/id<int:id_user>')
def about(id_user=None):
    if not 'id' in session and not id_user:
        return redirect('/')
    if 'id' in session:
        user = user_model.get_user_by_id(session.get('id'))[0]
        information = user_model.get_information(session.get('id'))
        sex_pref = user_model.get_sex_pref(session.get('id'))
        interests = user_model.get_interests_by_user_id(session.get('id'))

    if id_user:
        user = user_model.get_user_by_id(id_user)[0]
        information = user_model.get_information(id_user)
        sex_pref = user_model.get_sex_pref(id_user)
        interests = user_model.get_interests_by_user_id(id_user)

    data = {
        'user': user,
        'sympathys': sympathys,
        'information': information,
        'sex_pref': sex_pref,
        'interests': interests
    }
    return render_template('about.html', data=data)



# FRIENDS
@app.route('/profile/friends')
@app.route('/profile/friends/id<int:id_user>/')
def friends(id_user=None):
    if not 'id' in session and not id_user:
        return redirect('/')
    if 'id' in session:
        user = user_model.get_user_by_id(session.get('id'))[0]
        friends = sympathys.get_sympathys_list(session.get('id'))

    if id_user:
        user = user_model.get_user_by_id(id_user)[0]
        friends = sympathys.get_sympathys_list(id_user)
        image = user_model.get_avatar(session.get('id'))
        msg = str(session.get('firstname')) + ' ' + str(session.get(
            'lastname')) + ' viewed your profile.'
        notification_view.add_notification(id_user, msg, 'view', image)
    data = {
        'user': user,
        'sympathys': sympathys.get_sympathys_list(session.get('id')),
        'friends': friends,
        'get_user_by_id': user_model.get_user_by_id
    }
    return render_template('friends.html', data=data)

    # if 'id' in session:
    #     data = {
    #         'user': user_model.get_user_by_id(session.get('id'))[0],
    #         'sympathys': sympathys.get_sympathys_list(session.get('id')),
    #         'get_user_by_id': user_model.get_user_by_id
    #     }
    #     return render_template('friends.html', data=data)
    # return redirect('/')





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
    city = request.form['city']
    country = request.form['country']
    gender = request.form['gender']
    sex_pref = request.form['sex_pref']
    information = html.escape(request.form['information'])

    id = session.get('id')
    user = user_model.get_user_by_id(id)[0]
    if not gender:
        gender = user['gender']
    if not sex_pref:
        sex_pref = user['sex_pref']
    if not email:
        email = user['email']
    if not city:
        city = user['city']
    if not country:
        country = user['country']

    if (len(firstname) < 2) or (len(firstname) > 25):
        return json.dumps({
            'ok': False,
            'error': "Firstname length must be from 2 characters to 25",
            'fields': ["firstname"]
        })

    if (len(lastname) < 2) or (len(lastname) > 25):
        return json.dumps({
            'ok': False,
            'error': "Lastname length must be from 2 characters to 25",
            'fields': ["lastname"]
        })

    if not re.match("^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$", email.lower()):
        return json.dumps({
            'ok': False,
            'error': "Wrong email",
            'fields': ["email"]
        })
    res = user_model.change_basic(id, firstname, lastname, email, city, country, gender, sex_pref)
    if information:
        res1 = user_model.change_information(information, id)

    if not res and not res1:
        return json.dumps({
            'ok': True,
            'error': "Changes successfully saved"
        })
    else:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
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
        if res == 'exists':
            return json.dumps({
                'ok': False,
                'error': "Interest exists",
            })
        else:
            id_interest = user_model.get_interest_by_title(interest)[0]['id_interest']
            return json.dumps({
                'ok': True,
                'error': "Interest successfully added",
                'interest': interest,
                'icon': icon,
                'id_interest': id_interest
            })


@app.route('/ajax_delete_interest', methods=['POST'])
def ajax_delete_interest():
    id_interest = request.form['id_interest']
    id_user = session.get('id')

    if user_model.delete_interest(id_interest, id_user):
        return json.dumps({
            'ok': True,
            'error': "Interest deleted"
        })
    else:
        return json.dumps({
            'ok': False,
            'error': " Something went wrong. Interest not deleted."
        })



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
