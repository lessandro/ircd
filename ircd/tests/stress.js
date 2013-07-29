var WebSocket = require('ws');

var choice = function (a) {
    var r = (Math.random()*2000000000)|0;
    return a[r % a.length];
};

var new_client = function() {
    var ws = new WebSocket('ws://localhost:8888/sjs/websocket');
    var chans = [];

    var send = function() {
        var args = Array.prototype.slice.call(arguments);
        var data = args.join(' ') + '\r\n';
        ws.send(data);
        //console.log('> ' + data.trim());
    };

    ws.on('open', function() {
        send('NICK zxc' + ((Math.random()*1000)|0));
        send('USER u');
    });

    ws.on('message', function(data, flags) {
        //console.log('< ' + data.trim());
    });

    var do_something = function() {
        r = Math.random();

        if (chans.length < 3)
            r = 0;

        if (r < 0.1) {
            ch = '#' + ((Math.random()*10)|0);
            send('JOIN', ch);
            chans.push(ch);
        }
        else if (r < 0.2) {
            ch = choice(chans);
            send('PART', ch);
            chans.splice(chans.indexOf(ch), 1);
        }
        else {
            ch = choice(chans);
            send('PRIVMSG', ch, ':heloooooo nurse');
        }
    };

    setInterval(do_something, 500);
};

var n = process.argv[2]|0;
while (n--)
    new_client();
