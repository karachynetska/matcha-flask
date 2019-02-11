var socket = io.connect('http://' + document.domain + ':' + location.port);
var socket_messages = io.connect('http://' + document.domain + ':' + location.port + '/messages');

var id_dialogue,
    from_whom_id,
    to_whom_id;

function init(dialogue, id_user1, id_user2) {
    id_dialogue = dialogue;
    from_whom_id = id_user1;
    to_whom_id = id_user2;
    //     console.log(id_dialogue);
    // console.log(from_whom_id);
    // console.log(to_whom_id);
    socket_messages.emit('join_dialogue', {'id_dialogue': id_dialogue, 'from_whom_id': from_whom_id, 'to_whom_id': to_whom_id});
};

$('#send_message').on('click', function (e) {
    e.preventDefault();

    var message = $('#message').val();
    if (!message) {
        return;
    }
    var data = {'message': message, 'from_whom_id': from_whom_id, 'to_whom_id': to_whom_id};
    socket_messages.emit('send_message', data);
    $('message').val('');

});

socket_messages.on('add_message_to_template', function (data) {
   var from_whom_id = data['from-whom_id'],
       user = data['user'],
       last_message = data['last_message'];

   // var dialogue = $('#contact-'+data['dialogue']);
    console.log(data['dialogue']);
    console.log(data['from_whom_id']);
    console.log($('li.active').find('.from_whom_id').text());

   if(data['from_whom_id'] == $('li.active').find('.from_whom_id').text()) {
       $('#contact-'+data['dialogue']).find('.chat-message').append('<li class="right">\n' +
       '                      \t\t\t<img src="'+ user['avatar'] +'" alt="" class="profile-photo-sm pull-right" />\n' +
       '                      \t\t\t<div class="chat-item">\n' +
       '                              <div class="chat-item-header">\n' +
       '                              \t<h5>'+ user['firstname'] +' '+ user['lastname'] +'</h5>\n' +
       '                              \t<small class="text-muted">3 days ago</small>\n' +
       '                              </div>\n' +
       '                              <p>'+ data['message'] +'</p>\n' +
       '                            </div>\n' +
       '                      \t\t</li>');
   } else {
       console.log('else0');
       $('#contact-'+data['dialogue']).find('.chat-message').append('<li class="left">\n' +
       '                      \t\t\t<img src="'+ user['avatar'] +'" alt="" class="profile-photo-sm pull-right" />\n' +
       '                      \t\t\t<div class="chat-item">\n' +
       '                              <div class="chat-item-header">\n' +
       '                              \t<h5>'+ user['firstname'] +' '+ user['lastname'] +'</h5>\n' +
       '                              \t<small class="text-muted">3 days ago</small>\n' +
       '                              </div>\n' +
       '                              <p>'+ data['message'] +'</p>\n' +
       '                            </div>\n' +
       '                      \t\t</li>');
   }
   $("#"+data['dialogue']).find('#last_message').text('');
   $("#"+data['dialogue']).find('#last_message').text(last_message['message']);
});







