from app import app
from flask import request, session
import json
from app.models import user as user_model
from app.models import photos as photos_model
from app.views import notifications as notification_view
from app.models import sympathys
@app.route('/ajax_like_user')
def ajax_like_user():
    user_id = request.args.get('user_id')
    if photos_model.get_photos_nbr_by_id(session.get('id')) > 0:
        if photos_model.get_photos_nbr_by_id(user_id) < 1:
            return json.dumps({
                'ok': False,
                'error': "To like a user, he must have at least one photo uploaded"
            })
        check = sympathys.check_request(session.get('id'), user_id)
        if not check:
            res = sympathys.like_user(session.get('id'), user_id)
            if res:
                msg = str(session.get('firstname')) + ' ' + str(session.get('lastname')) + ' likes you!'
                image = user_model.get_avatar(session.get('id'))
                notification_view.add_notification(session.get('id'), user_id, msg, 'like_user', image)
                rating = user_model.get_user_fame_rating(user_id) + 20
                user_model.update_user_rating(rating, user_id)
                return json.dumps({
                'ok': True,
                'error': "Liked"
                })
            else:
                return json.dumps({
                    'ok': False,
                    'error': "Something went wrong"
                })
        else:
            return json.dumps({
                'ok': False,
                'error': "It's your friend"
            })
    else:
        return json.dumps({
            'ok': False,
            'error': "To like a user, you must have at least one photo uploaded"
        })

@app.route('/ajax_pick_up_like')
def ajax_pick_up_like():
    user_id = request.args.get('user_id')
    if not sympathys.check_sympathy(session.get('id'), user_id):
        if sympathys.check_request(session.get('id'), user_id) == 'sender':
            if sympathys.check_request_status(session.get('id'), user_id)[0]['status'] == 0:
                if sympathys.remove_request(session.get('id'), user_id) == []:
                    rating = user_model.get_user_fame_rating(user_id) - 20
                    user_model.update_user_rating(rating, user_id)
                    return json.dumps({
                        'ok': True,
                        'error': "Pick_up_like"
                    })
                else:
                    return json.dumps({
                        'ok': False,
                        'error': "Something went wrong"
                    })
            else:
                return json.dumps({
                    'ok': False,
                    'error': "Something went wrong"
                })
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })
    else:
        return json.dumps({
            'ok': False,
            'error': "It's your friend"
        })

@app.route('/ajax_like_back_user')
def ajax_like_back_user():
    user_id = request.args.get('user_id')
    if not sympathys.check_sympathy(session.get('id'), user_id):
        sympathys.like_back_user(session.get('id'), user_id)
        sympathys.add_users_to_sympathys(session.get('id'), user_id)

        msg = 'You like each other! Now you can chat with ' + str(session.get('firstname')) + ' ' + str(session.get('lastname')) + '.'
        image = user_model.get_avatar(session.get('id'))
        notification_view.add_notification(session.get('id'), user_id, msg, 'like_back_user', image)
        rating = user_model.get_user_fame_rating(user_id) + 20
        user_model.update_user_rating(rating, user_id)
        return json.dumps({
            'ok': True,
            'error': "Liked_back"
        })

@app.route('/ajax_unlike_user')
def ajax_delete_friend():
    user_id = request.args.get('user_id')
    if sympathys.check_sympathy(session.get('id'), user_id):
        if sympathys.check_request(session.get('id'), user_id) == 'sender':
            sympathys.remove_request(session.get('id'), user_id)
            status = 'sender'
        else:
            status = 'taker'
            sympathys.set_request_status_to_zero(session.get('id'), user_id)
        if not sympathys.unlike_user(session.get('id'), user_id):
            msg = str(session.get('firstname')) + ' ' + str(session.get('lastname')) + ' does not like you anymore.'
            image = user_model.get_avatar(session.get('id'))
            notification_view.add_notification(session.get('id'), user_id, msg, 'unlike_user', image)
            rating = user_model.get_user_fame_rating(user_id) - 20
            user_model.update_user_rating(rating, user_id)
            return json.dumps({
                'ok': True,
                'error': "Unlike",
                'status': status
            })
        else:
            return json.dumps({
                'ok': False,
                'error': "Something went wrong"
            })
    else:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })

@app.route('/ajax_report')
def ajax_report():
    user_id = request.args.get('user_id')
    if sympathys.report_user(user_id):
        return json.dumps({
            'ok': True,
            'error': "Report"
        })
    else:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })

@app.route('/ajax_block')
def ajax_block():
    user_id = request.args.get('user_id')
    my_id = session.get('id')
    if sympathys.block_user(user_id, my_id):
        if sympathys.check_request(session.get('id'), user_id) == 'sender':
            sympathys.remove_request(session.get('id'), user_id)
        else:
            sympathys.remove_request(user_id, session.get('id'))
        if not sympathys.unlike_user(user_id, my_id):
            return json.dumps({
                'ok': True,
                'error': "Block"
            })
        else:
            return json.dumps({
                'ok': False,
                'error': "Something went wrong"
            })
    else:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })

@app.route('/ajax_unblock')
def ajax_unblock():
    user_id = request.args.get('user_id')
    my_id = session.get('id')
    if sympathys.check_block(user_id, my_id):
        if not sympathys.unblock_user(user_id, my_id):
            return json.dumps({
                'ok': True,
                'error': "Unblock"
            })
        else:
            return json.dumps({
                'ok': False,
                'error': "Something went wrong"
            })
    else:
        return json.dumps({
            'ok': False,
            'error': "This user is not blocked"
        })

@app.route('/ajax_decline')
def ajax_decline():
    user_id = request.args.get('user_id')
    print(user_id)

    if not sympathys.check_sympathy(session.get('id'), user_id):
        print('not sympathy')
        sympathys.remove_request(user_id, session.get('id'))
        return json.dumps({
            'ok': True,
            'error': "Decline"
        })
    else:
        return json.dumps({
            'ok': False,
            'error': "Something went wrong"
        })