import logging
import tornado.gen
import tornado.netutil
import tornadoredis
from client import Client


class Server(tornado.netutil.TCPServer):
    def __init__(self, io_loop, config):
        super(Server, self).__init__(io_loop)

        self.port = config.tcp_port
        self.init_redis(io_loop)

    @tornado.gen.engine
    def init_redis(self, io_loop):
        # this connection pushes messages to the input queue
        self.redis_in = tornadoredis.Client(io_loop=io_loop)
        self.redis_in.connect()

        # this connection listens for messages from the output channel
        self.redis_out = tornadoredis.Client(io_loop=io_loop)
        self.redis_out.connect()
        yield tornado.gen.Task(self.redis_out.subscribe, 'output')
        self.redis_out.listen(self.handle_message)

    def start(self):
        logging.info('Starting IRCd server on port \'%d\'', self.port)
        self.listen(self.port)

    def handle_stream(self, stream, address):
        client = Client(stream, address, self.redis_in)
        client.on_connect()

    def handle_message(self, msg):
        if msg.kind == 'message':
            print 'output:', msg.body
