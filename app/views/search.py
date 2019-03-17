from app import app
from flask import render_template, request, session, redirect
import json
from app.models import user as user_model
from app.models import search as search_model
from app.models import geolocation as geolocation_model
from app.models import messages as messages_model
from datetime import datetime, date
from math import sin, cos, sqrt, atan2, radians

@app.route('/profile/search')
def search():
    if not 'id' in session:
        return redirect('/')
    data = {
        'user': user_model.get_user_by_id(session.get('id'))[0],
        'unread_messages_nbr': messages_model.get_unread_messages_nbr_by_user_id(session.get('id'))
    }
    return render_template('search.html', data=data)

def calculate_distance(latitude, longitude):
    if latitude == None or longitude == None:
        return None
    geolocation = geolocation_model.get_geolocation_by_user_id(session.get('id'))
    if geolocation:
        my_latitude = float(geolocation['latitude'])
        my_longitude = float(geolocation['longitude'])

        R = 6373.0

        latitude = radians(latitude)
        longitude = radians(longitude)
        my_latitude = radians(my_latitude)
        my_longitude = radians(my_longitude)

        dlon = my_longitude - longitude
        dlat = my_latitude - latitude

        a = sin(dlat / 2) ** 2 + cos(latitude) * cos(my_latitude) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance

    else:
        return None

@app.route('/ajax_search', methods=['POST'])
def ajax_search():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    from_age = request.form['from_age']
    to_age = request.form['to_age']
    from_rate = request.form['from_rate']
    to_rate = request.form['to_rate']
    gender = request.form['gender']
    country = request.form['country']
    city = request.form['city']
    interest1 = request.form['interest1']
    interest2 = request.form['interest2']
    interest3 = request.form['interest3']
    interest4 = request.form['interest4']
    filter = request.form['filter']
    sort = request.form['sort']

    my_id = session.get('id')
    users = []
    if first_name and last_name:
        users = search_model.search_by_full_name(my_id, first_name, last_name)

    if first_name and not last_name:
        users = search_model.search_by_first_name(my_id, first_name)

    if last_name and not first_name:
        users = search_model.search_by_last_name(my_id, last_name)

    if not first_name and not last_name:
        users = search_model.search(session.get('id'))

    found_users = []

    for user in users:
        correct = True
        user['age'] = date.today().year - datetime.strptime(user['birth_date'], '%Y-%m-%d %H:%M:%S').year
        geolocation = geolocation_model.get_geolocation_by_user_id(user['id'])
        if geolocation:
            user['latitude'] = float(geolocation['latitude'])
            user['longitude'] = float(geolocation['longitude'])
        else:
            user['latitude'] = None
            user['longitude'] = None
        user['distance'] = calculate_distance(user['latitude'], user['longitude'])
        if filter == 'distance' and not user['distance']:
            correct = False
        if from_age or to_age:
            if from_age:
                if user['age'] < int(from_age):
                    correct = False
            if to_age:
                if user['age'] > int(to_age):
                    correct = False
        if from_rate:
            if user['fame_rating'] < from_rate:
                correct = False
        if to_rate:
            if user['fame_rating'] > to_rate:
                correct = False
        if gender and gender != 'all':
            if user['gender'].find(gender) == -1:
                correct = False
        if country:
            if user['country'].find(country) == -1:
                correct = False
        if city:
            if user['city'].find(city) == -1:
                correct = False

        # INTERESTS
        if interest1 or interest2 or interest3 or interest4:
            interests = user_model.get_interests_by_user_id(user['id'])
            user['interests'] = []
            user['interests_nbr'] = 0
            for interest in interests:
                user['interests'].append(interest['title'])
            if interest1:
                if not interest1 in user['interests']:
                    correct = False
                else:
                    user['interests_nbr'] += 1
            if interest2:
                if not interest2 in user['interests']:
                    correct = False
                else:
                    user['interests_nbr'] += 1
            if interest3:
                if not interest3 in user['interests']:
                    correct = False
                else:
                    user['interests_nbr'] += 1
            if interest4:
                if not interest4 in user['interests']:
                    correct = False
                else:
                    user['interests_nbr'] += 1

        if correct:
            found_users.append(user)

# FILTER
    if found_users and filter:
        if filter == 'age' and sort == 'asc':
            found_users = sorted(found_users, key=lambda k: k['age'])
        if filter == 'age' and sort == 'desc':
            found_users = sorted(found_users, key=lambda k: k['age'], reverse=True)
        if filter == 'distance' and sort == 'asc':
            found_users = sorted(found_users, key=lambda k: k['distance'])
        if filter == 'distance' and sort == 'desc':
            found_users = sorted(found_users, key=lambda k: k['distance'], reverse=True)
        if filter == 'rating' and sort == 'asc':
            found_users = sorted(found_users, key=lambda k: k['rating'])
        if filter == 'rating' and sort == 'desc':
            found_users = sorted(found_users, key=lambda k: k['rating'], reverse=True)
        if interest1 or interest2 or interest3 or interest4:
            if filter == 'interests' and sort == 'asc' and found_users[0]['interests_nbr']:
                found_users = sorted(found_users, key=lambda k: k['interests_nbr'])
            if filter == 'interests' and sort == 'desc' and found_users[0]['interests_nbr']:
                found_users = sorted(found_users, key=lambda k: k['interests_nbr'], reverse=True)

    if not found_users:
        return json.dumps({
            'ok': False,
            'error': 'No matches.'
        })
    return json.dumps({
            'ok': True,
            'found_users': found_users
        })