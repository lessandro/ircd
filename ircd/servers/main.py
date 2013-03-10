import logging
import tornado.ioloop


def main(server_types, config):
    logging.getLogger().setLevel(logging.INFO)
    servers = []

    if 'tcp' in server_types:
        import tcpserver
        servers.append(tcpserver.TCPServer(config))

    if 'sio' in server_types:
        import sioserver
        servers.append(sioserver.SioServer(config))

    try:
        logging.info('Starting ioloop')
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        for server in servers:
            server.stop()
