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

$('#add_friend').on('click', function (e) {
    e.preventDefault();

    var url = getLocation(location.href);
    var user_id = url.pathname.match(/(\d+)/)[1];
    var data = {
        user_id: user_id
    };

    $.get('/ajax_add_friend', data).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == true) {
            $('#add_friend').html('Pending');
            $('#add_friend').attr('id', 'pending');
        }
    });
});

$('#delete_friend').on('click', function (e) {
    e.preventDefault();
    console.log('pressed')

    var url = getLocation(location.href);
    var user_id = url.pathname.match(/(\d+)/)[1];
    var data = {
        user_id: user_id
    };

    $.get('/ajax_delete_friend', data).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == true) {
            $('#delete_friend').html('Add Friend');
            $('#delete_friend').attr('id', 'add_friend');
        }
    });
});