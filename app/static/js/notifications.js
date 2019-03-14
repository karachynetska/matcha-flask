$(document).ready(function () {
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var socket_notifications = io('http://' + document.domain + ':' + location.port + '/notifications');

    socket_notifications.on('notification', function (data) {
        if (data) {
            console.log(data);
            jQuery.each(data, function (i, val) {
                $('.notifications').append('<li class="notification-li"><div class="notification"><img src="'+val['image']+'" alt="user" class="profile-photo-md pull-left notification-img"/><p>'+val['notification']+'</p></div></li>');
            });
        }
        swipe();
    });

    function swipe() {
        $('.notification-li').draggable({
            axis: "x"
        });
        $('.notification-li').bind("mouseup mouseleave", function() {
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
            } else {
                $(this).animate({
                    left: 0
                });
            }
        });
    }
});
