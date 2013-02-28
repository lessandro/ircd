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
        yield tornado.gen.Task(self.server.connect)

        logging.info('Starting IRCd server on port \'%d\'', config.tcp_port)
        self.listen(config.tcp_port)

    def handle_stream(self, stream, address):
        tag = self.server.make_tag(address[0], address[1])
        on_data = functools.partial(self.handle_data, tag)
        stream.read_until_close(on_data, on_data)

        def handler(data):
            if data:
                stream.write(data)
            else:
                stream.close()

        self.server.user_connect(tag, address[0], handler)

    def handle_data(self, tag, data):
        if data:
            self.server.user_message(tag, data)
        else:
            self.server.user_disconnect(tag)
