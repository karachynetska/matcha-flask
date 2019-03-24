from app import app
from flask import render_template, redirect, request, session
from flask_uploads import configure_uploads, IMAGES, UploadSet, UploadNotAllowed
from datetime import datetime
import json
from app.models import user as user_model
from app.models import photos as photos_model
from app.models import likes, comments
from app.models import messages as messages_model
from app.views import notifications as notification_view
from app.models import sympathys
from app.views.notifications import get_online_users


images = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = "app/static/media"
configure_uploads(app, images)


@app.route('/profile/photos')
@app.route('/profile/photos/id<int:id_user>/')
def photos(id_user=None):
    if not 'id' in session and not id_user:
        return redirect('/')
    if 'id' in session:
        id = session.get('id')
        user = user_model.get_user_by_id(id)[0]
        photos = photos_model.get_photos_by_id(id)

    if id_user:
        if not user_model.get_user_by_id(id_user):
            return render_template('404.html')
        if sympathys.check_block(id_user, session.get('id')):
            return redirect('/profile/id'+ str(id_user))
        user = user_model.get_user_by_id(id_user)[0]
        photos = photos_model.get_photos_by_id(id_user)


    data = {
        'user': user,
        'photos': photos,
        'get_user_by_id': user_model.get_user_by_id,
        'get_avatar': user_model.get_avatar,
        'likes': likes.photo_likes,
        'dislikes': likes.photo_dislikes,
        'check_like': likes.check_like,
        'check_dislike': likes.check_dislike,
        'get_comments_by_photo_id': comments.get_comments_by_photo_id,
        'unread_messages_nbr': messages_model.get_unread_messages_nbr_by_user_id(session.get('id')),
        'incoming_requests_nbr': sympathys.get_incoming_requests_nbr(session.get('id')),
        'online_users': get_online_users()
    }

    return render_template('photos.html', data=data)


@app.route('/ajax_add_photo', methods=["POST"])
def ajax_add_photo():
    photo = request.files.get('photo')

    if not photo:
        return json.dumps({
            'ok': False,
            'error': "Something wrong"
        })

    if photos_model.get_photos_nbr_by_id(session.get('id')) < 4:
        login = session.get('login')
        extension = photo.filename.rsplit('.', 1)[1]
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        photo_name = str(login + date + '.' + extension)
        path = '/static/media/' + login + '/' + photo_name
        try:
            images.save(photo, login, photo_name)
        except UploadNotAllowed:
            return json.dumps({
                'ok': False,
                'error': "Extension not allowed"
            })
        # images.save(photo, login, photo_name)
        photos_model.add_photo(session.get('id'), path)

        rating = user_model.get_user_fame_rating(session.get('id')) + 10
        user_model.update_user_rating(rating, session.get('id'))

        return json.dumps({
            'ok': True,
            'error': "Photo successfully uploaded"
        })
    else:
        return json.dumps({
            'ok': False,
            'error': "You have the maximum number of photos"
        })

@app.route('/ajax_delete_photo', methods=['POST'])
def ajax_delete_photo():
    id_photo = request.form['id_photo']

    if not id_photo:
        return json.dumps({
            'ok': False,
            'error': 'Something wrong'
        })
    photos_model.delete_photo_by_id(id_photo)
    rating = user_model.get_user_fame_rating(session.get('id')) - 10
    user_model.update_user_rating(rating, session.get('id'))
    return json.dumps({
        'ok': True,
        'error': 'Photo deleted'
    })