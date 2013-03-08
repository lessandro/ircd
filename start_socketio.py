#!/usr/bin/env python

import logging
import tornado.ioloop
from servers.sioserver import SioServer
import config

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    server = SioServer(config)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        server.stop()
