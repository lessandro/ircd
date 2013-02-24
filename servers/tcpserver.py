import logging
import functools
import tornado.gen
import tornado.netutil
from server import Server


class TCPServer(tornado.netutil.TCPServer):
    @tornado.gen.engine
    def __init__(self, config):
        super(TCPServer, self).__init__()

        self.server = Server('tcp')

        logging.info('Starting IRCd server on port \'%d\'', config.tcp_port)
        self.listen(config.tcp_port)

    def handle_stream(self, stream, address):
        tag = '%s-%d' % (address[0], address[1])
        on_data = functools.partial(self.user_data, tag)
        stream.read_until_close(on_data, on_data)
        self.server.user_connect(tag, address[0])

    def user_data(self, tag, data):
        if not data:
            self.server.user_disconnect(tag)
            return

        # TODO: buffer, split lines
        self.server.user_message(tag, data.strip())
