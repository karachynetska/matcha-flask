var socket = io.connect('http://' + document.domain + ':' + location.port);
var socket_messages = io.connect('http://' + document.domain + ':' + location.port + '/messages');