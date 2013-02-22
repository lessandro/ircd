import tornado
import tornadio2
from .. import util


class Connection(tornadio2.conn.SocketConnection):
    def init(self, redis):
        self.redis = redis

    def on_open(self, info):
        print 'connect'

    def on_message(self, data):
        print 'message', data
        self.redis.rpush('input', data.decode('utf-8').strip())

    def on_close(self):
        print 'disconnect'


class Server(object):
    @tornado.gen.engine
    def __init__(self, io_loop, config):
        (self.redis_in, self.redis_out), _ = yield tornado.gen.Task(
            util.init_redis, io_loop, self.handle_message)
        self.init_socketio(io_loop, config)

    def init_socketio(self, io_loop, config):
        def conn_maker(session):
            conn = Connection(session)
            conn.init(self.redis_in)
            return conn

        router = tornadio2.TornadioRouter(conn_maker, io_loop=io_loop)

        app = tornado.web.Application(
            router.urls,
            flash_policy_file=config.flash_policy_file,
            flash_policy_port=config.flash_policy_port,
            socket_io_port=config.socketio_port)

        tornadio2.SocketServer(app, auto_start=False, io_loop=io_loop)

    def handle_message(self, msg):
        if msg.kind == 'message':
            print 'output:', msg.body
