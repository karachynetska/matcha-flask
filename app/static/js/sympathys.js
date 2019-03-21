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
    var url = getLocation(location.href);
    var user_id = url.pathname.match(/(\d+)/)[1];
    var data = {
        user_id: user_id
    };

    $.get('/ajax_like_user', data).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == true) {
            $('#like_user').parent().addClass('none');
            $('#liked_user').parent().removeClass('none');
            $('#like_user_M').parent().addClass('none');
            $('#liked_user_M').parent().removeClass('none');
        } else {
            alert(res.error);
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

// REPORT

function report() {
    var url = getLocation(location.href),
        user_id = url.pathname.match(/(\d+)/)[1],
        data = {
        user_id: user_id
    };

    $.get('/ajax_report', data).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == true) {

        } else {

        }
    });
}

$('#report_user').on('click', function (e) {
    e.preventDefault();

    report();
});

$('#report_user_M').on('click', function (e) {
    e.preventDefault();

    report();
});

// BLOCK

function block() {
    var url = getLocation(location.href),
        user_id = url.pathname.match(/(\d+)/)[1],
        data = {
        user_id: user_id
    };

    $.get('/ajax_block', data).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == true) {
            console.log(res.error);
            $('#actions').addClass('none');
            $('#actions_M').addClass('none');
            $('#like_user').parent().addClass('none');
            $('#like_user_M').parent().addClass('none');
            $('#liked_user').parent().addClass('none');
            $('#liked_user_M').parent().addClass('none');
            $('#unlike_user').parent().addClass('none');
            $('#unlike_user_M').parent().addClass('none');
            $('#like_back').parent().addClass('none');
            $('#like_back_M').parent().addClass('none');
            $('#start_dialogue').parent().parent().addClass('none');
            $('#start_dialogue_M').parent().parent().addClass('none');
            $('.actions').append('<li id="block"><a style="color: #ff374f; text-decoration: none;">Blocked by you</a></li>');
            $('.actions_M').append('<li id="block_M"><a style="color: #ff374f; text-decoration: none;">Blocked by you</a></li>');
        } else {
            console.log(res.error);
        }
    });

}

$('#block_user').on('click', function (e) {
    e.preventDefault();

    block();
});

$('#block_user_M').on('click', function (e) {
    e.preventDefault();

    block();
});

// UNBLOCK

function unblock() {
    var url = getLocation(location.href),
        user_id = url.pathname.match(/(\d+)/)[1],
        data = {
        user_id: user_id
    };

    $.get('/ajax_unblock', data).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == true) {
            $('#block').addClass('none');
            $('#block_M').addClass('none');
            $('#unblock_user').addClass('none');
            $('#unblock_user_M').addClass('none');
            $('#like_user').parent().removeClass('none');
            $('#like_user_M').parent().removeClass('none');
            $('#actions').removeClass('none');
            $('#actions_M').removeClass('none');
        } else {
            console.log(res.error);
        }
    });
}

$('#unblock_user').on('click', function (e) {
    e.preventDefault();

    unblock();
});


$('#unblock_user_M').on('click', function (e) {
    e.preventDefault();

    unblock();
});