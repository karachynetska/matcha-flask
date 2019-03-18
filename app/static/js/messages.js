window.onload = function () {
    $('.scrollbar-wrapper').scrollHeight = 999999999999;
};
var socket = io.connect('http://' + document.domain + ':' + location.port);
var socket_messages = io('http://' + document.domain + ':' + location.port + '/messages');

var id_dialogue,
    from_whom_id,
    to_whom_id;

function init(dialogue, id_user1, id_user2) {
    id_dialogue = dialogue;
    from_whom_id = id_user1;
    to_whom_id = id_user2;
    var nbr =  $('#'+id_dialogue).find('.chat-alert').text();
    var nbr1 = $('#unread_messages_nbr').text();
    nbr = parseInt(nbr, 10);
    nbr1 = parseInt(nbr1, 10);
    nbr1 = nbr1 - nbr;
    if (nbr1 === 0) {
        $('#unread_messages_nbr').addClass('none');
    } else {
        $('#unread_messages_nbr').removeClass('none');
        $('#unread_messages_nbr').text(nbr1);
    }
    $('#'+id_dialogue).find('.chat-alert').addClass('none');
    socket_messages.emit('join_dialogue', {'id_dialogue': id_dialogue, 'from_whom_id': from_whom_id, 'to_whom_id': to_whom_id});
    $('.send_message').removeClass('none');
}

$('#send_message').on('click', function (e) {
    e.preventDefault();

    var message = $('#message').val();
    if (!message) {
        return;
    }
    var data = {'message': message, 'from_whom_id': from_whom_id, 'to_whom_id': to_whom_id};
    socket_messages.emit('send_message', data);
    $('#message').val('');
});

socket_messages.on('add_message_to_template', function (data) {
   var user = data['user'],
       last_message = data['last_message'];

   console.log(data['last_message']);
   console.log(data['dialogue']);
   console.log(data['from_whom_id']);
   console.log($('li.active').find('.from_whom_id').text());

   if(data['from_whom_id'] == $('li.active').find('.from_whom_id').text()) {
       $('#contact-'+data['dialogue']).find('.chat-message').append('<li class="right">\n' +
       '                      \t\t\t<a href="/profile/id'+user['id']+'"><img src="'+ user['avatar'] +'" alt="" class="profile-photo-sm pull-right" /></a>\n' +
       '                      \t\t\t<div class="chat-item">\n' +
       '                              <div class="chat-item-header">\n' +
       '                              \t<h5>'+ user['firstname'] +' '+ user['lastname'] +'</h5>\n' +
       '                              \t<small class="text-muted">3 days ago</small>\n' +
       '                              </div>\n' +
       '                              <p>'+ data['message'] +'</p>\n' +
       '                            </div>\n' +
       '                      \t\t</li>');
   } else {
       $('#contact-'+data['dialogue']).find('.chat-message').append('<li class="left">\n' +
       '                      \t\t\t<a href="/profile/id'+user['id']+'"><img src="'+ user['avatar'] +'" alt="" class="profile-photo-sm pull-left" /></a>\n' +
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
   $("#"+data['dialogue']).find('#last_message').text(data['message']);
   console.log(data['to_whom_id']);
   console.log(data['my_id']);
   if (data['to_whom_id'] == data['my_id']) {
       console.log('blah');
       var nbr = $('#'+data['dialogue'].find('.chat-alert').text());
        nbr = parseInt(nbr, 10);
        nbr += 1;
        $('#'+data['dialogue']).find('.chat-alert').removeClass('none');
        $('#'+data['dialogue']).find('.chat-alert').text(nbr);

        var nbr1 = $('#unread_messages_nbr').text();
        nbr1 = parseInt(nbr1, 10);
        nbr1 += 1;
        $('#unread_messages_nbr').removeClass('none');
        $('#unread_messages_nbr').text(nbr1);
   }

   topPos = $('.chat-message').offsetTop;
   $('#message_scroll').scrollTop = topPos;
});

socket_messages.on('add_unread_message', function (data) {
    console.log('blah');
    var nbr = $('#'+data['dialogue'].find('.chat-alert').text());
    nbr = parseInt(nbr, 10);
    nbr += 1;
    $('#'+data['dialogue']).find('.chat-alert').removeClass('none');
    $('#'+data['dialogue']).find('.chat-alert').text(nbr);

    var nbr1 = $('#unread_messages_nbr').text();
    nbr1 = parseInt(nbr1, 10);
    nbr1 += 1;
    $('#unread_messages_nbr').removeClass('none');
    $('#unread_messages_nbr').text(nbr1);
});

var dialogue_id = $('#dialogue_id').text();
if (dialogue_id !== "None") {
    console.log(dialogue_id);
    $('#'+dialogue_id).addClass('active');
    $('#'+dialogue_id).find('a').attr('area-expanded', 'true');
    $('#contact-'+dialogue_id).addClass('active');
    $('.send_message').removeClass('none');
}








