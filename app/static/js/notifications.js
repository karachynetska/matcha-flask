var socket = io.connect('http://' + document.domain + ':' + location.port);
var socket_notifications = io.connect('http://' + document.domain + ':' + location.port + '/notifications');

socket_notifications.on('notifications', function (data) {
    var notifications = $('.notifications');
    console.log(notifications);
    if (data) {
        console.log(data);
        // notifications.append('<li><div class="notification"><img src="" alt="user" class="profile-photo-md pull-left notification-img"/><h1>Notification with icon</h1> <p>lorem ipsum dolor sit amet</p></div></li>')
    }
});

$('.notification').draggable({
 axis: "x"
});
$('.notification').bind("mouseup mouseleave", function() {
 if ($(this).position().left >= 80) {
  $(this).animate({
    left: 400,
    opacity: 0
   }, 200,
   function() {
    $(this).html('');
    $(this).animate({
      padding: 0,
      height: 0,
      margin: 0
     }, 500,
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
 // <li><div class="notification"> <img src="{{ data.user.avatar }}" alt="user" class="profile-photo-md pull-left notification-img"/><h1>Notification with icon</h1> <p>lorem ipsum dolor sit amet</p></div></li>