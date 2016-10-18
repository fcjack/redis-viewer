$(document).ready(function(){
    var namespace = "/redis";
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

    socket.on('connect', function(){
        socket.emit('message', {data: "Hello, connected"});
    });
});