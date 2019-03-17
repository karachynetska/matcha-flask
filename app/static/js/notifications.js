function delete_notification(id_notification) {
    var data = {
        'id_notification': id_notification
    };

    $.ajax({
        type: 'POST',
        data: data,
        url: '/ajax_delete_notification'
    }).done(function (data) {
        var res = JSON.parse(data);
        if (res.ok == false) {
            console.log(res.error);
        } else {
            console.log(res.error);
        }
    });
}

$(document).ready(function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var socket_notifications = io('http://' + document.domain + ':' + location.port + '/notifications');

    socket_notifications.on('notification', function (data) {
        if (data) {
            console.log(data);
            
            jQuery.each(data, function (i, val) {
                $('.notifications').append('<li id="notification-'+val['id_notification']+'" class="notification-li"><div class="notification"><img src="'+val['image']+'" alt="user" class="profile-photo-md pull-left notification-img"/><p>'+val['notification']+'</p></div></li>');
                if (val['notif_type'] == 'message') {
                    console.log('yes');
                    var nbr = $('#unread_messages_nbr').text();
                    nbr = parseInt(nbr, 10);
                    nbr += 1;
                    $('#unread_messages_nbr').removeClass('none');
                    $('#unread_messages_nbr').text(nbr);
                }
                swipe(val['id_notification']);
            setTimeout(function () {
                $('#notification-'+val['id_notification']+'').remove();
                delete_notification(val['id_notification']);
            }, 60000); //will be deleted in a minute
            });
        }

    });

    function swipe(id_notification) {
        $('#notification-'+id_notification).draggable({
            axis: "x"
        });
        $('#notification-'+id_notification).bind("mouseup mouseleave", function() {
            if ($(this).position().left >= 80) {
                $(this).animate({
                        left: 400,
                        opacity: 0
                    },200,
                    function() {
                    $(this).html('');
                    $(this).animate({
                            padding: 0,
                            height: 0,
                            margin: 0
                        },500,
                        function() {
                        $(this).remove();
                    });
                });
                delete_notification(id_notification);
            } else {
                $(this).animate({
                    left: 0
                });
            }
        });
    }
});
