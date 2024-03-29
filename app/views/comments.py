from app import app
from flask import request, session
import html

import json

from app.models import user as user_model
from app.models import comments
from app.views import notifications as notifications_view


@app.route('/ajax_add_comment', methods=["POST"])
def ajax_add_comment():
    id_photo = request.form['id_photo']
    id_user = session.get('id')
    text = html.escape(request.form['text'])

    if not id_photo or not id_user or not text:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })
    res = comments.add_comment(id_photo, id_user, text)
    to_whom_id = user_model.get_user_id_by_photo_id(id_photo)
    if to_whom_id != session.get('id'):
        msg = 'You have a new comment from ' + str(session.get('firstname')) + ' ' + str(session.get('lastname')) + '.'
        image = user_model.get_avatar(session.get('id'))
        notifications_view.add_notification(session.get('id'), to_whom_id, msg, 'comment', image)
    rating = user_model.get_user_fame_rating(to_whom_id) + 5
    user_model.update_user_rating(rating, to_whom_id)
    if not res:
        return json.dumps({
            'ok': False,
            'error': "The comment has not been added"
        })
    return json.dumps({
        'ok': True,
        'error': "Commented",
        'id_comment': res,
        'text': text
    })

@app.route('/ajax_delete_comment', methods=['POST'])
def ajax_delete_comment():
    id_comment = request.form['id_comment']
    if not id_comment:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })
    res = comments.delete_comment(id_comment)
    if not res:
        return json.dumps({
            'ok': True,
            'error': "Comment deleted",
        })
    else:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })