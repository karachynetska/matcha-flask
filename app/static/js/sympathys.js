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

// LIKE USER
function like_user() {
    console.log('pressed');
    var url = getLocation(location.href);
    var user_id = url.pathname.match(/(\d+)/)[1];
    var data = {
        user_id: user_id
    };

    $.get('/ajax_like_user', data).done(function (data) {
        var res = JSON.parse(data);
        console.log(res);
        if (res.ok == true) {
            $('#like_user').parent().addClass('none');
            $('#liked_user').parent().removeClass('none');
            $('#like_user_M').parent().addClass('none');
            $('#liked_user_M').parent().removeClass('none');
        }
    });
}

$('#like_user').on('click', function (e) {
    e.preventDefault();

    like_user();
});


$('#like_user_M').on('click', function (e) {
    e.preventDefault();
    console.log('pressedM');
    like_user();
});


// PICK UP LIKE
function pick_up_like() {
    var url = getLocation(location.href);
    var user_id = url.pathname.match(/(\d+)/)[1];
    var data = {
        user_id: user_id
    };

    $.get('/ajax_pick_up_like', data).done(function (data) {
        var res = JSON.parse(data);
        console.log(res);
        if (res.ok == true) {
            $('#liked_user').parent().addClass('none');
            $('#like_user').parent().removeClass('none');
            $('#liked_user_M').parent().addClass('none');
            $('#like_user_M').parent().removeClass('none');
        }
    });
}

$('#liked_user').on('click', function (e) {
    e.preventDefault();

    pick_up_like();
});

$('#liked_user_M').on('click', function (e) {
    e.preventDefault();

    pick_up_like();
});


// UNLIKE USER
function unlike_user() {
    var url = getLocation(location.href);
    var user_id = url.pathname.match(/(\d+)/)[1];
    var data = {
        user_id: user_id
    };

    $.get('/ajax_unlike_user', data).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == true) {
            $('#unlike_user').parent().addClass('none');
            $('#like_user').parent().removeClass('none');
            $('#start_dialogue').parent().parent().addClass('none');
            $('#unlike_user_M').parent().addClass('none');
            $('#like_user_M').parent().removeClass('none');
            $('#start_dialogue_M').parent().parent().addClass('none');
        }
    });
}

$('#unlike_user').on('click', function (e) {
    e.preventDefault();

    unlike_user();
});

$('#unlike_user_M').on('click', function (e) {
    e.preventDefault();

    unlike_user();
});

// LIKE BACK

function like_back() {
    var url = getLocation(location.href);
    var user_id = url.pathname.match(/(\d+)/)[1];
    var data = {
        user_id: user_id
    };

    $.get('/ajax_like_back_user', data).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == true) {
            $('#like_back').parent().addClass('none');
            $('#unlike_user').parent().removeClass('none');
            $('#start_dialogue').parent().parent().removeClass('none');
            $('#like_back_M').parent().addClass('none');
            $('#unlike_user_M').parent().removeClass('none');
            $('#start_dialogue_M').parent().parent().removeClass('none');

            var nbr = $('#incoming_requests_nbr').text();
            nbr = parseInt(nbr, 10);
            var nbr1 = nbr - 1;
            if (nbr1 <= 0) {
                $('#incoming_requests_nbr').addClass('none');
            } else {
                $('#incoming_requests_nbr').text(nbr1);
            }
        }
    });
}

$('#like_back').on('click', function (e) {
    e.preventDefault();

    like_back();
});

$('#like_back_M').on('click', function (e) {
    e.preventDefault();

    like_back();
});