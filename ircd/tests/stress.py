import tornado.ioloop
import tornado.iostream
import socket
import random
import sys

address = ('localhost', 5556)


class Client(object):
    def __init__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        self.stream = tornado.iostream.IOStream(s)
        self.stream.connect(address, self.on_connect)
        self.stream.read_until('\n', self.on_data)
        self.chans = set()

        self.timer = tornado.ioloop.PeriodicCallback(self.do_something, 500)
        self.timer.start()

    def send(self, *args):
        self.stream.write(' '.join(args) + '\r\n')

    def on_connect(self):
        self.send('NICK py' + str(random.randint(0, 1000)))
        self.send('USER u\n')

    def on_data(self, data):
        self.stream.read_until('\n', self.on_data)

    def do_something(self):
        r = random.random()
        if len(self.chans) < 3:
            r = 0

        if r < 0.1:
            ch = '#' + str(random.randint(0, 10))
            self.send('JOIN', ch)
            self.chans.add(ch)
        elif r < 0.2:
            ch = random.choice(list(self.chans))
            self.send('PART', ch)
            self.chans.remove(ch)
        else:
            ch = random.choice(list(self.chans))
            self.send('PRIVMSG', ch, ':heloooooo nurse')


for _ in xrange(int(sys.argv[1])):
    Client()

tornado.ioloop.IOLoop.instance().start()
