function like(id_photo, id_user) {
    var data = {
        id_photo: id_photo,
        id_user: id_user
    },
        $like = $('.like.photo-'+id_photo),
        $count = $('.like.photo-'+id_photo+' span')[0],
        $pop_like = $('.pop-like.photo-'+id_photo),
        $pop_count = $('.pop-like.photo-'+id_photo+' span')[0],

        $dislike = $('.dislike.photo-'+id_photo),
        $count_dislike = $('.dislike.photo-'+id_photo+' span')[0],
        $pop_dislike = $('.pop-dislike.photo-'+id_photo),
        $pop_count_dislike = $('.pop-dislike.photo-'+id_photo+' span')[0];

    $.ajax({
        type: 'POST',
        data: data,
        url: '/ajax_like'
    }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == false) {
            $like.removeClass('text-green');
            $like.addClass('text-muted');
            $count.innerText = parseInt($count.innerText) - 1;

            $pop_like.removeClass('text-green');
            $pop_like.addClass('text-muted');
            $pop_count.innerText = parseInt($pop_count.innerText) - 1;
        } else {
            if (res.error == 'Was dislike') {
                $dislike.removeClass('text-red');
                $dislike.addClass('text-muted');
                $count_dislike.innerText = parseInt($count_dislike.innerText) - 1;

                $pop_dislike.removeClass('text-red');
                $pop_dislike.addClass('text-muted');
                $pop_count_dislike.innerText = parseInt($pop_count_dislike.innerText) - 1;
            }
            $like.removeClass('text-muted');
            $like.addClass('text-green');
            $count.innerText = parseInt($count.innerText) + 1;

            $pop_like.removeClass('text-muted');
            $pop_like.addClass('text-green');
            $pop_count.innerText = parseInt($pop_count.innerText) + 1;
        }
    });
}

function dislike(id_photo, id_user) {
    var data = {
        id_photo: id_photo,
        id_user: id_user
    },
        $dislike = $('.dislike.photo-'+id_photo),
        $count = $('.dislike.photo-'+id_photo+' span')[0],
        $pop_dislike = $('.pop-dislike.photo-'+id_photo),
        $pop_count = $('.pop-dislike.photo-'+id_photo+' span')[0],

        $like = $('.like.photo-'+id_photo),
        $count_like = $('.like.photo-'+id_photo+' span')[0],
        $pop_like = $('.pop-like.photo-'+id_photo),
        $pop_count_like = $('.pop-like.photo-'+id_photo+' span')[0];

    $.ajax({
        type: 'POST',
        data: data,
        url: '/ajax_dislike'
    }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == false) {
            $dislike.removeClass('text-red');
            $dislike.addClass('text-muted');
            $count.innerText = parseInt($count.innerText) - 1;

            $pop_dislike.removeClass('text-red');
            $pop_dislike.addClass('text-muted');
            $pop_count.innerText = parseInt($pop_count.innerText) - 1;
        } else {
            if (res.error == 'Was like') {
                $like.removeClass('text-green');
                $like.addClass('text-muted');
                $count_like.innerText = parseInt($count_like.innerText) - 1;

                $pop_like.removeClass('text-green');
                $pop_like.addClass('text-muted');
                $pop_count_like.innerText = parseInt($pop_count_like.innerText) - 1;
            }
            $dislike.removeClass('text-muted');
            $dislike.addClass('text-red');
            $count.innerText = parseInt($count.innerText) + 1;

            $pop_dislike.removeClass('text-muted');
            $pop_dislike.addClass('text-red');
            $pop_count.innerText = parseInt($pop_count.innerText) + 1;
        }
    });
}


// FOR NEWSFEED

function newsfeed_like(id_photo, id_user) {
    var data = {
        id_photo: id_photo,
        id_user: id_user
    },
        $like = $('.like.photo-'+id_photo),
        $count = $('.like.photo-'+id_photo+' span')[0],

        $dislike = $('.dislike.photo-'+id_photo),
        $count_dislike = $('.dislike.photo-'+id_photo+' span')[0];

    $.ajax({
        type: 'POST',
        data: data,
        url: '/ajax_like'
    }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == false) {
            $like.removeClass('text-green');
            $like.addClass('text-muted');
            $count.innerText = parseInt($count.innerText) - 1;

        } else {
            if (res.error == 'Was dislike') {
                $dislike.removeClass('text-red');
                $dislike.addClass('text-muted');
                $count_dislike.innerText = parseInt($count_dislike.innerText) - 1;
            }
            $like.removeClass('text-muted');
            $like.addClass('text-green');
            $count.innerText = parseInt($count.innerText) + 1;
        }
    });
}

function newsfeed_dislike(id_photo, id_user) {
    var data = {
        id_photo: id_photo,
        id_user: id_user
    },
        $dislike = $('.dislike.photo-'+id_photo),
        $count = $('.dislike.photo-'+id_photo+' span')[0],

        $like = $('.like.photo-'+id_photo),
        $count_like = $('.like.photo-'+id_photo+' span')[0];

    $.ajax({
        type: 'POST',
        data: data,
        url: '/ajax_dislike'
    }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == false) {
            $dislike.removeClass('text-red');
            $dislike.addClass('text-muted');
            $count.innerText = parseInt($count.innerText) - 1;
        } else {
            if (res.error == 'Was like') {
                $like.removeClass('text-green');
                $like.addClass('text-muted');
                $count_like.innerText = parseInt($count_like.innerText) - 1;
            }
            $dislike.removeClass('text-muted');
            $dislike.addClass('text-red');
            $count.innerText = parseInt($count.innerText) + 1;
        }
    });
}