function add_comment(form) {
    event.preventDefault();
    var id_photo = form.id_photo.value,
        text = form.comment.value,
        id_user = form.id_user.value,
        data = {
        id_photo: id_photo,
        text: text
    };

    $.ajax({
        type: "POST",
        data: data,
        url: "/ajax_add_comment"
    }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == false) {
            console.log(res.error);
        } else {
            var profile_photo = $('#profile_photo').val(),
                user_firstname = $('#user_firstname').val();

            $('.modal-'+id_photo).find('#photo_comments').append('<div class="post-comment" id="comment-'+res.id_comment+'"><img src="'+ profile_photo + '" alt="" class="profile-photo-sm" /><p><a href="/profile/id'+id_user+'" class="profile-link">'+user_firstname+' </a> '+res.text+' <br><a id="delete_comment" class="text-muted" style="text-decoration: none;" onclick="delete_comment('+ res.id_comment +')">Delete</a></p></div>');
            $('#photo_comments-'+id_photo).append('<div class="post-comment" id="comment-'+res.id_comment+'"><img src="'+ profile_photo + '" alt="" class="profile-photo-sm" /><p><a href="/profile/id'+id_user+'" class="profile-link">'+user_firstname+' </a> '+res.text+' <br><a id="delete_comment" class="text-muted" style="text-decoration: none;" onclick="delete_comment('+ res.id_comment +')">Delete</a></p></div>');
            form.reset();
        }
        $('#photo_comments').scrollTop(9999);
    });
}


function delete_comment(id_comment) {
    event.preventDefault();
    var data = {
        'id_comment': id_comment
    };

    $.ajax({
        type: 'POST',
        data: data,
        url: '/ajax_delete_comment'
    }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == false) {
            console.log(res.error)
        } else {
            $('#comment-'+id_comment).remove();
        }
    });
}
