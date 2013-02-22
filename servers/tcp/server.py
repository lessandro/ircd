import logging
import tornado.gen
import tornado.netutil
from client import Client
from .. import util


class Server(tornado.netutil.TCPServer):
    @tornado.gen.engine
    def __init__(self, io_loop, config):
        super(Server, self).__init__(io_loop)
        (self.redis_in, self.redis_out), _ = yield tornado.gen.Task(
            util.init_redis, io_loop, self.handle_message)
        self.init_tcp(config)

    def init_tcp(self, config):
        logging.info('Starting IRCd server on port \'%d\'', config.tcp_port)
        self.listen(config.tcp_port)

    def handle_stream(self, stream, address):
        client = Client(stream, address, self.redis_in)
        client.on_connect()

    def handle_message(self, msg):
        if msg.kind == 'message':
            print 'output:', msg.body
