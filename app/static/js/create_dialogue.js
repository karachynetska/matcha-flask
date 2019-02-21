function start_dialogue(id_user1, id_user2) {
    var data = {
    id_user1: id_user1,
    id_user2: id_user2
    };

    $.ajax({
        type: 'POST',
        data: data,
        url: '/ajax_start_dialogue'
    }).done(function (data) {
        var res = JSON.parse(data);
    });
}
