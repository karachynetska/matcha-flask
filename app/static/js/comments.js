function add_comment(form) {
    event.preventDefault();
    var data = {
        id_photo: form.id_photo.value,
        text: form.comment.value
    };
    id_photo = data.id_photo;
    console.log(data.text);

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
                user_firstname = $('#user_firstname').val(),
                comment = $('#comment').val();

            console.log(profile_photo);
            console.log(user_firstname);

            // var div = document.createElement('div');
            // div.addClass('post-comment');
            // var img = document.createElement('img');
            // img.addClass('profile-photo-sm');
            // var p = document.createElement('p');
            // p.text(data['text']);
            // var a = document.createElement('a');
            // a.text(user_firstname);
            // a.addClass('profile-link');
            // p.appendChild(a);
            // div.appendChild(img);
            // div.appendChild(p);
            $('.modal-'+id_photo).find('#photo_comments').append('<div class="post-comment"><img src="'+ profile_photo + '" alt="" class="profile-photo-sm" /><p><a href="timeline.html" class="profile-link">' + user_firstname + '</a> ' + comment +'</p></div>');
            // $('#photo_comments').append('<div class="post-comment"><img src="'+ profile_photo + '" alt="" class="profile-photo-sm" /><p><a href="timeline.html" class="profile-link">' + user_firstname + '</a> ' + comment +'</p></div>');
            form.reset();
        }
    });
}


// <div class="post-comment" id="comment-{{ comment.id_comment }}">
//     <img src="{{ user.avatar }}" alt="" class="profile-photo-sm" />
//     <p><a href="timeline.html" class="profile-link">{{ user.firstname }} </a> {{ comment.text }} </p>
// </div>