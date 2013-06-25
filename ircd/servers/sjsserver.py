import functools
import tornado
import sockjs.tornado
from server import Server


class Connection(sockjs.tornado.SockJSConnection):
    def __init__(self, server, *kargs, **kwargs):
        super(Connection, self).__init__(*kargs, **kwargs)
        self.server = server

    def on_open(self, info):
        self.tag = self.server.make_tag(info.ip, id(self))

        def handler(data):
            if data:
                self.send(data.decode('utf-8'))
            else:
                self.close()

        self.server.user_connect(self.tag, info.ip, handler)

    def on_message(self, message):
        self.server.user_message(self.tag, message.encode('utf-8'))

    def on_close(self):
        self.server.user_disconnect(self.tag)


class SjsServer(object):
    @tornado.gen.engine
    def __init__(self, config):
        self.server = Server('sjs', config)
        yield tornado.gen.Task(self.server.connect)

        conn_maker = functools.partial(Connection, self.server)

        router = sockjs.tornado.SockJSRouter(conn_maker, '/sjs')

        app = tornado.web.Application(router.urls)
        app.listen(config.sockjs_port)

    def stop(self):
        self.server.stop()
