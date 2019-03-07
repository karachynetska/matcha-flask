from app import app
from flask import render_template, request, session, redirect
import json
from app.models import user as user_model

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

    return "response"