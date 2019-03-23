from app import app
from flask import render_template, redirect, request, session
from flask_uploads import configure_uploads, IMAGES, UploadSet
import html
import hashlib
from datetime import datetime, date
import json, re, os
from app.models import user as user_model
from app.models import geolocation as geolocation_model
from app.views import notifications as notification_view
from app.models import notifications as notification_model
from app.models import sympathys
from app.models import likes, comments
from app.models import suggestions as suggestions_model
from app.models import photos as photos_model
from app.models import messages as messages_model
from app.views.search import calculate_distance
from app.views.notifications import get_online_users, get_offline_users
from app.settings import APP_ROOT

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = "app/static/media"
configure_uploads(app, photos)


def get_suggestions_for_user(user):
    suggestions = []

    if user['gender'] == 'Female' and user['sex_pref'] == 'Heterosexual':
        suggestions = suggestions_model.get_getero_or_bi_man(user['id'])

    if user['gender'] == 'Female' and user['sex_pref'] == 'Homosexual':
        suggestions = suggestions_model.get_homo_or_bi_women(user['id'])

    if user['gender'] == 'Female' and user['sex_pref'] == 'Bisexual':
        suggestions = suggestions_model.get_users_for_bi_woman(user['id'])

    if user['gender'] == 'Male' and user['sex_pref'] == 'Heterosexual':
        suggestions = suggestions_model.get_getero_or_bi_women(user['id'])

    if user['gender'] == 'Male' and user['sex_pref'] == 'Homosexual':
        suggestions = suggestions_model.get_homo_or_bi_man(user['id'])

    if user['gender'] == 'Male' and user['sex_pref'] == 'Bisexual':
        suggestions = suggestions_model.get_users_for_bi_man(user['id'])

    return suggestions

# PROFILE
@app.route('/profile')
@app.route('/profile/id<int:id_user>/')
def profile(id_user=None):
    if not 'id' in session:
        return redirect('/')
    if 'id' in session:
        my_id = session.get('id')
        user = user_model.get_user_by_id(my_id)[0]
        friends = sympathys.get_sympathys_list(my_id)
        information = user_model.get_information(my_id)
        interests = user_model.get_interests_by_user_id(my_id)
        education = user_model.get_education_by_user_id(my_id)
        work = user_model.get_work_by_user_id(my_id)
        geolocation = geolocation_model.get_geolocation_by_user_id(my_id)


    if id_user:
        if not user_model.get_user_by_id(id_user):
            return render_template('404.html')
        user = user_model.get_user_by_id(id_user)[0]
        friends = sympathys.get_sympathys_list(id_user)
        information = user_model.get_information(id_user)
        interests = user_model.get_interests_by_user_id(id_user)
        education = user_model.get_education_by_user_id(id_user)
        work = user_model.get_work_by_user_id(id_user)
        geolocation = geolocation_model.get_geolocation_by_user_id(id_user)

        if id_user != session.get('id'):
            msg = str(session.get('firstname')) + ' ' + str(session.get('lastname')) + ' viewed your profile.'
            image = user_model.get_avatar(session.get('id'))
            notification_view.add_notification(session.get('id'), id_user, msg, 'view', image)

    user['age'] = date.today().year - datetime.strptime(user['birth_date'], '%Y-%m-%d %H:%M:%S').year

    data = {
        'user': user,
        'friends': friends,
        'sympathys': sympathys,
        'information': information,
        'interests': interests,
        'education': education,
        'work': work,
        'geolocation': geolocation,
        'unread_messages_nbr': messages_model.get_unread_messages_nbr_by_user_id(session.get('id')),
        'incoming_requests_nbr': sympathys.get_incoming_requests_nbr(session.get('id')),
        'check_block': sympathys.check_block,
        'offline_users': get_offline_users(),
        'online_users': get_online_users()
    }
    return render_template('profile.html', data=data)



# FRIENDS
@app.route('/profile/friends')
@app.route('/profile/friends/id<int:id_user>/')
def friends(id_user=None):
    if not 'id' in session and not id_user:
        return redirect('/')
    if 'id' in session:
        user = user_model.get_user_by_id(session.get('id'))[0]
        friends = sympathys.get_sympathys_list(session.get('id'))
        incoming_requests = sympathys.get_incoming_requests(session.get('id'))
        outgoing_requests = sympathys.get_outgoing_requests(session.get('id'))
        blocked_users = sympathys.get_blocked_users(session.get('id'))

    if id_user:
        if not user_model.get_user_by_id(id_user):
            return render_template('404.html')
        if sympathys.check_block(id_user, session.get('id')):
            return redirect('/profile/id'+ str(id_user))
        user = user_model.get_user_by_id(id_user)[0]
        friends = sympathys.get_sympathys_list(id_user)
        incoming_requests = None
        outgoing_requests = None
        blocked_users = None

    data = {
        'user': user,
        'sympathys': sympathys,
        'friends': friends,
        'get_user_by_id': user_model.get_user_by_id,
        'incoming_requests': incoming_requests,
        'outgoing_requests': outgoing_requests,
        'unread_messages_nbr': messages_model.get_unread_messages_nbr_by_user_id(session.get('id')),
        'incoming_requests_nbr': sympathys.get_incoming_requests_nbr(session.get('id')),
        'blocked_users': blocked_users,
        'check_block': sympathys.check_block,
        'offline_users': get_offline_users(),
        'online_users': get_online_users()
    }
    return render_template('friends.html', data=data)


# SUGGESTIONS
@app.route('/profile/suggestions')
def suggestions():
    if not 'id' in session:
        return redirect('/')
    user = user_model.get_user_by_id(session.get('id'))[0]
    selected = get_suggestions_for_user(user)
    suggestions = []
    for suggestion in selected:
        correct = True
        if sympathys.check_block(suggestion['id'], session.get('id')):
            correct = False
        geolocation = geolocation_model.get_geolocation_by_user_id(suggestion['id'])
        if geolocation:
            suggestion['latitude'] = float(geolocation['latitude'])
            suggestion['longitude'] = float(geolocation['longitude'])
        else:
            suggestion['latitude'] = None
            suggestion['longitude'] = None
        suggestion['distance'] = calculate_distance(suggestion['latitude'], suggestion['longitude'])
        if suggestion['distance'] is None:
            correct = False
        my_interests = user_model.get_interests_by_user_id(session.get('id'))
        suggestion['interests_nbr'] = 0
        if my_interests:
            interests = user_model.get_interests_by_user_id(suggestion['id'])
            if interests:
                my_tags = []
                for my_interest in my_interests:
                    my_tags.append(my_interest['title'])
                for interest in interests:
                    if interest['title'] in my_tags:
                        suggestion['interests_nbr'] += 1
        if correct:
            suggestions.append(suggestion)
        suggestions = sorted(suggestions, key=lambda k: k['distance'])
        suggestions = sorted(suggestions, key=lambda k: k['interests_nbr'], reverse=True)
        suggestions = sorted(suggestions, key=lambda k: k['fame_rating'], reverse=True)
    data = {
        'user': user,
        'suggestions': suggestions,
        'unread_messages_nbr': messages_model.get_unread_messages_nbr_by_user_id(session.get('id')),
        'incoming_requests_nbr': sympathys.get_incoming_requests_nbr(session.get('id')),
        'friends': sympathys.get_sympathys_list(session.get('id')),
        'online_users': get_online_users()
    }
    return render_template('suggestions.html', data = data)


# NOTIFICATIONS
@app.route('/profile/notifications')
def notifications():
    if not 'id' in session:
        return redirect('/')
    user = user_model.get_user_by_id(session.get('id'))[0]
    notifications = notification_model.get_notification_by_user_id(session.get('id'))
    if notifications:
        notifications = sorted(notifications, key=lambda k: k['date_of_creation'], reverse=True)

    data = {
        'user': user,
        'unread_messages_nbr': messages_model.get_unread_messages_nbr_by_user_id(session.get('id')),
        'incoming_requests_nbr': sympathys.get_incoming_requests_nbr(session.get('id')),
        'notifications': notifications,
        'online_users': get_online_users(),
        'get_user_by_id': user_model.get_user_by_id,
    }
    return render_template('notifications.html', data=data)



# NEWSFEED
@app.route('/newsfeed')
def newsfeed():
    if 'id' in session:
        my_id = session.get('id')
        friends = sympathys.get_sympathys_list(my_id)
        photos = []
        if friends:
            for friend in friends:
                if friend['id_user1'] == my_id:
                    photos = photos_model.get_photos_by_id(friend['id_user2'])
                else:
                    photos = photos_model.get_photos_by_id(friend['id_user1'])
            if photos:
                photos = sorted(photos, key=lambda k: k['date_added'], reverse=True)
        data = {
            'user': user_model.get_user_by_id(my_id)[0],
            'get_user_by_id': user_model.get_user_by_id,
            'get_avatar': user_model.get_avatar,
            'unread_messages_nbr': messages_model.get_unread_messages_nbr_by_user_id(my_id),
            'incoming_requests_nbr': sympathys.get_incoming_requests_nbr(my_id),
            'check_like': likes.check_like,
            'check_dislike': likes.check_dislike,
            'photos': photos,
            'likes': likes.photo_likes,
            'dislikes': likes.photo_dislikes,
            'get_comments_by_photo_id': comments.get_comments_by_photo_id,
            'online_users': get_online_users(),
            'friends': sympathys.get_sympathys_list(session.get('id')),
        }
        return render_template('newsfeed.html', data=data)
    return redirect('/')


# EDIT BASIC INFORMATION
@app.route('/profile/edit/basic')
def edit_basic():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0],
            'unread_messages_nbr': messages_model.get_unread_messages_nbr_by_user_id(session.get('id')),
            'incoming_requests_nbr': sympathys.get_incoming_requests_nbr(session.get('id')),
            'friends': sympathys.get_sympathys_list(session.get('id'))
        }
        return render_template('edit-profile-basic.html', data=data)
    else:
        return redirect('/')

@app.route('/profile/edit/geolocation')
def edit_geolocation():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0],
            'geolocation': geolocation_model.get_geolocation_by_user_id(session.get('id')),
            'unread_messages_nbr': messages_model.get_unread_messages_nbr_by_user_id(session.get('id')),
            'incoming_requests_nbr': sympathys.get_incoming_requests_nbr(session.get('id')),
            'friends': sympathys.get_sympathys_list(session.get('id'))
        }
        return render_template('edit-profile-geolocation.html', data=data)
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
            'user': user_model.get_user_by_id(session.get('id'))[0],
            'unread_messages_nbr': messages_model.get_unread_messages_nbr_by_user_id(session.get('id')),
            'incoming_requests_nbr': sympathys.get_incoming_requests_nbr(session.get('id')),
            'friends': sympathys.get_sympathys_list(session.get('id'))
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
            'interests': user_model.get_interests_by_user_id(session.get('id')),
            'unread_messages_nbr': messages_model.get_unread_messages_nbr_by_user_id(session.get('id')),
            'incoming_requests_nbr': sympathys.get_incoming_requests_nbr(session.get('id')),
            'friends': sympathys.get_sympathys_list(session.get('id'))
        }
        return render_template('edit-profile-interests.html', data=data)
    else:
        return redirect('/')


@app.route('/ajax_edit_interests', methods=['POST'])
def ajax_edit_interests():
    interest = html.escape(request.form['interest'])
    icon = "fas fa-hashtag"

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
            'user': user_model.get_user_by_id(session.get('id'))[0],
            'unread_messages_nbr': messages_model.get_unread_messages_nbr_by_user_id(session.get('id')),
            'incoming_requests_nbr': sympathys.get_incoming_requests_nbr(session.get('id')),
            'friends': sympathys.get_sympathys_list(session.get('id'))
        }
        return render_template('edit-profile-edu-work.html', data=data)
    else:
        return redirect('/')


#CHANGE AVATAR
@app.route('/profile/edit/avatar')
def edit_avatar():
    if 'id' in session:
        data = {
            'user': user_model.get_user_by_id(session.get('id'))[0],
            'unread_messages_nbr': messages_model.get_unread_messages_nbr_by_user_id(session.get('id')),
            'incoming_requests_nbr': sympathys.get_incoming_requests_nbr(session.get('id')),
            'friends': sympathys.get_sympathys_list(session.get('id'))
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
        user_model.delete_avatar_from_db(avatar_name, id)
    else:
        rating = user['fame_rating'] + 42
        user_model.update_user_rating(rating, id)

    # SAVE AVATAR TO FOLDER
    photos.save(avatar, login, avatar_name)

    # CHANGE AVATAR IN DB
    if not user_model.change_avatar(path, id):
        photos_model.add_photo(id, path)
        return json.dumps({
            'ok': True,
            'error': 'Avatar successfully uploaded',
        })
    else:
        return json.dumps({
            'ok': False,
            'error': "Something wrong"
        })

@app.route('/ajax_add_education', methods=['POST'])
def ajax_edit_education():
    university = request.form['university']
    date_from = request.form['date_from']
    date_to = request.form['date_to']
    description = request.form['description']

    if not university:
        return json.dumps({
            'ok': False,
            'error': "Please fill in selected field",
            'fields': ['school']
        })

    if not date_from:
        return json.dumps({
            'ok': False,
            'error': "Please fill in selected field",
            'fields': ['date_from']
        })

    if not date_to:
        return json.dumps({
            'ok': False,
            'error': "Please fill in selected field",
            'fields': ['date_to']
        })

    if user_model.add_education(session.get('id'), university, date_from, date_to, description):
        rating = user_model.get_user_fame_rating(session.get('id')) + 15
        user_model.update_user_rating(rating, session.get('id'))
        return json.dumps({
            'ok': True,
            'error': "Education successfully added"
        })
    else:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })


@app.route('/ajax_delete_education', methods=['POST'])
def ajax_delete_education():
    id_education = request.form['id_education']
    if not id_education:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })
    if not user_model.delete_education(id_education):
        return json.dumps({
            'ok': True,
            'error': "Education deleted"
        })
    else:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })

@app.route('/ajax_add_work', methods=['POST'])
def ajax_edit_work():
    company = request.form['company']
    designation = request.form['designation']
    from_date = request.form['from_date']
    to_date = request.form['to_date']
    city = request.form['city']
    description = request.form['description']

    if not company:
        return json.dumps({
            'ok': False,
            'error': "Please fill in selected field",
            'fields': ['company']
        })

    if not designation:
        return json.dumps({
            'ok': False,
            'error': "Please fill in selected field",
            'fields': ['designation']
        })

    if not from_date:
        return json.dumps({
            'ok': False,
            'error': "Please fill in selected field",
            'fields': ['from_date']
        })

    if not to_date:
        return json.dumps({
            'ok': False,
            'error': "Please fill in selected field",
            'fields': ['to_date']
        })

    if not city:
        return json.dumps({
            'ok': False,
            'error': "Please fill in selected field",
            'fields': ['work_city']
        })

    if user_model.add_work(session.get('id'), company, designation, from_date, to_date, city, description):
        rating = user_model.get_user_fame_rating(session.get('id')) + 15
        user_model.update_user_rating(rating, session.get('id'))
        return json.dumps({
            'ok': False,
            'error': "Work successfully added"
        })
    else:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })

@app.route('/ajax_delete_work', methods=['POST'])
def ajax_delete_work():
    id_work = request.form['id_work']
    if not id_work:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })
    if not user_model.delete_work(id_work):
        return json.dumps({
            'ok': True,
            'error': "Work deleted"
        })
    else:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })