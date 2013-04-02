var io = require('socket.io-client');

var newClient = function(n) {
    var s = new io.connect('http://localhost:8001', {
        'rememberTransport': false,
        'force new connection': true
    });

    function send(data) {
        s.send(data + "\r\n");
    }

    s.on('connect', function() {
        console.log('connected');
        send('NICK おはよう' + n);
        send('USER user');
        send('JOIN #asd' + (n % 10));
    });

    s.on('message', function(data) {
        //console.log('message ' + data.trim());
    });

    s.on('disconnect', function() {
        console.log('disconnected');
    });

    var i = 0;
    var x = setInterval(function() {
        send("PRIVMSG #asd" + (n % 10) + " :hello " + i);
        if (i++ == 4) {
            try {
                s.disconnect();
            } catch (e) {

            }
            clearInterval(x);
        }
    }, 20);
};

(function() {
    var i = 0;
    var x = setInterval(function() {
        newClient(i);
        i++;
    }, 20);
})();
