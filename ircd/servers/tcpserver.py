import logging
import functools
import tornado.gen
import tornado.tcpserver
from server import Server


class TCPServer(tornado.tcpserver.TCPServer):
    @tornado.gen.engine
    def __init__(self, config):
        super(TCPServer, self).__init__()

        self.server = Server('tcp', config)
        yield tornado.gen.Task(self.server.connect)

        logging.info('Starting IRCd server on port \'%d\'', config.tcp_port)
        self.listen(config.tcp_port)

    def stop(self):
        self.server.stop()

    def handle_stream(self, stream, address):
        tag = self.server.make_tag(address[0], address[1])

        u_handler = functools.partial(self.handle_user_data, tag)
        stream.read_until_close(u_handler, u_handler)

        s_handler = functools.partial(self.handle_server_data, tag, stream)
        self.server.user_connect(tag, address[0], s_handler)

    def handle_user_data(self, tag, data):
        if data:
            self.server.user_message(tag, data)
        else:
            self.server.user_disconnect(tag)

    def handle_server_data(self, tag, stream, data):
        try:
            if data:
                # this might fail if the connection is closed
                stream.write(data)
            else:
                stream.close()
        except:
            # close and notify closed
            try:
                stream.close()
            finally:
                self.server.user_disconnect(tag)
