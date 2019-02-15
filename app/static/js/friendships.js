function getLocation(href) {
    var match = href.match(/^(https?\:)\/\/(([^:\/?#]*)(?:\:([0-9]+))?)([\/]{0,1}[^?#]*)(\?[^#]*|)(#.*|)$/);
    return match && {
        href: href,
        protocol: match[1],
        host: match[2],
        hostname: match[3],
        port: match[4],
        pathname: match[5],
        search: match[6],
        hash: match[7]
    }
}

$('#like_user').on('click', function (e) {
    e.preventDefault();

    var url = getLocation(location.href);
    var user_id = url.pathname.match(/(\d+)/)[1];
    var data = {
        user_id: user_id
    };

    $.get('/ajax_like_user', data).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == true) {
            $('#like_user').html('Liked');
            $('#like_user').addClass('liked_user');
            $('#like_user').attr('id', 'liked_user');
        }
    });
});

$('#unlike_user').on('click', function (e) {
    e.preventDefault();
    console.log('pressed')

    var url = getLocation(location.href);
    var user_id = url.pathname.match(/(\d+)/)[1];
    var data = {
        user_id: user_id
    };

    $.get('/ajax_unlike_user', data).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == true) {
            $('#unlike_user').html('Like');
            $('#unlike_user').addClass('like_user');
            $('#unlike_user').attr('id', 'like_user');
        }
    });
});

$('#like_back').on('click', function (e) {
    e.preventDefault();

    var url = getLocation(location.href);
    var user_id = url.pathname.match(/(\d+)/)[1];
    var data = {
        user_id: user_id
    };

    $.get('/ajax_like_back_user', data).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == true) {
            $('#like_back').html('Unlike');
            $('#like_back').addClass('unlike_user');
            $('.actions').append('<li><button id="send_message" class="btn-primary">Send message</button></li>');
            $('#like_back').attr('id', 'unlike_user');
        }
    });
});