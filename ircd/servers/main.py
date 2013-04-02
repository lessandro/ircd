import time
import signal
import logging
import tornado.ioloop

servers = []


def sig_handler(sig, frame):
    for server in servers:
        server.stop()

    io_loop = tornado.ioloop.IOLoop.instance()
    io_loop.add_timeout(time.time() + 0.01, io_loop.stop)


def main(server_types, config):
    logging.getLogger().setLevel(logging.INFO)

    if 'tcp' in server_types:
        import tcpserver
        servers.append(tcpserver.TCPServer(config))

    if 'sio' in server_types:
        import sioserver
        servers.append(sioserver.SioServer(config))

    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    logging.info('Starting ioloop')
    tornado.ioloop.IOLoop.instance().start()
