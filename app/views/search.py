from app import app
from flask import render_template, request, session, redirect
import json
from app.models import user as user_model
from app.models import search as search_model
from datetime import datetime, date

@app.route('/profile/search')
def search():
    if not 'id' in session:
        return redirect('/')
    data = {
        'user': user_model.get_user_by_id(session.get('id'))[0]
    }
    return render_template('search.html', data=data)


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

    print(first_name)
    print(last_name)
    print(from_age)
    print(to_age)
    print(from_rate)
    print(to_rate)
    print(gender)
    print(country)
    print(city)
    print(interest1)
    print(interest2)
    print(interest3)
    print(interest4)

    my_id = session.get('id')
    users = []
    if first_name and last_name:
        users = search_model.search_by_full_name(my_id, first_name, last_name)

    if first_name and not last_name:
        print('firstname')
        users = search_model.search_by_first_name(my_id, first_name)

    if last_name and not first_name:
        users = search_model.search_by_last_name(my_id, last_name)

    if not first_name and not last_name:
        users = search_model.search(session.get('id'))

    found_users = []

    print(users)

    for user in users:
        correct = True
        if from_age or to_age:
            user['age'] = date.today().year - datetime.strptime(user['birth_date'], '%Y-%m-%d %H:%M:%S').year
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

        if correct:
            found_users.append(user)
    return json.dumps({
            'ok': True,
            'found_users': found_users
        })