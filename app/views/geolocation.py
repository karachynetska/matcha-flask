from app import app
from flask import request, session
import json
from app.models import geolocation as geolocation_model


@app.route('/ajax_set_geolocation', methods=['POST'])
def ajax_set_geolocation():
    id_user = session.get('id')
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    if not latitude or not longitude:
        latitude = 50.4688257
        longitude = 30.4621588

    if geolocation_model.add_geolocation(id_user, latitude, longitude):
        return json.dumps({
            'ok': True,
            'error': "Geolocation saved.",
        })

@app.route('/ajax_change_geolocation', methods=['POST'])
def ajax_change_geolocation():
    id_user = session.get('id')
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    if not geolocation_model.change_geolocation(id_user, latitude, longitude):
        return json.dumps({
            'ok': True,
            'error': "Your geolocation successfully changed.",
        })
    else:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong.",
        })