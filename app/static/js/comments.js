function add_comment(form) {
    event.preventDefault();
    var id_photo = form.id_photo.value,
        text = form.comment.value,
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

            $('.modal-'+id_photo).find('#photo_comments').append('<div class="post-comment"><img src="'+ profile_photo + '" alt="" class="profile-photo-sm" /><p><a href="timeline.html" class="profile-link">' + user_firstname + '</a> ' + text +'</p></div>');
            form.reset();
        }
    });
}
