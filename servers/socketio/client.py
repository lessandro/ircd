import tornado
import tornadio2
from user import User


class Client(User):
    def __init__(self, ircd, connection, info):
        super(SioUser, self).__init__(ircd)

        self.connection = connection
        self.address = info.ip

    def send(self, message):
        self.connection.send(message)

    def disconnect(self):
        self.connection.close()


class Connection(tornadio2.conn.SocketConnection):
    def on_open(self, info):
        self.user = SioUser(self.ircd, self, info)
        self.user.on_connect()

    def on_message(self, data):
        self.user.on_data(data)

    def on_close(self):
        self.user.on_disconnect()


class SioServer(object):
    def __init__(self, ircd, io_loop, config):
        def conn_maker(session):
            conn = Connection(session)
            conn.ircd = ircd
            return conn

        router = tornadio2.TornadioRouter(conn_maker, io_loop=io_loop)

        application = tornado.web.Application(
            router.urls,
            flash_policy_file=config.flash_policy_file,
            flash_policy_port=config.flash_policy_port,
            socket_io_port=config.socket_io_port
        )

        tornadio2.SocketServer(
            application,
            auto_start=False,
            io_loop=io_loop
        )
