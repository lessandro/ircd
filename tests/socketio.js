var io = require('socket.io-client');

var s = new io.connect('http://localhost:8001', {
    rememberTransport: false
});

function send(data) {
    s.send(data + "\r\n");
}

s.on('connect', function() {
    console.log('connected');
    send('おはよう');
});

s.on('message', function(data) {
    console.log('message ' + data.trim());
});

s.on('disconnect', function() {
    console.log('disconnected');
});

var i = 0;
var x = setInterval(function() {
    send("u craz " + i);
    if (i++ == 4) {
        s.disconnect();
        clearInterval(x);
    }
}, 1000);
