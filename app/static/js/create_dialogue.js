var user1_id,
    user2_id,
    id_dialogue;

function start_chat(id_user1, id_user2) {
    console.log('in function');
    user1_id = id_user1;
    user2_id = id_user2;
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
        if (res.ok == true) {
            id_dialogue = res.id_dialogue;
            location.replace('/profile/messages');
        } else {
            console.log('Something went wrong');
        }
    });
}

if (location.pathname == '/profile/messages') {
    $(window).on('load', function () {
        console.log(id_dialogue);
        console.log($('.contact-list').find('#'+id_dialogue));

    });
    // console.log($('.contact-list'));
    // $('#'+id_dialogue).addClass('active');
}

