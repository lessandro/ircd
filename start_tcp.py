import logging
import tornado.ioloop
from servers.tcp.server import Server
import config

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    io_loop = tornado.ioloop.IOLoop.instance()
    server = Server(io_loop, config)
    server.start()
    io_loop.start()
