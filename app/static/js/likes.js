function like(id_photo, id_user) {
    var data = {
        id_photo: id_photo,
        id_user: id_user
    };
    $.ajax({
        type: 'POST',
        data: data,
        url: '/ajax_like'
    }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == false) {

        } else {

        }
    });
}

function dislike(id_photo, id_user) {
    var data = {
        id_photo: id_photo,
        id_user: id_user
    };
    $.ajax({
        type: 'POST',
        data: data,
        url: '/ajax_dislike'
    }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == false) {

        } else {

        }
    });
}