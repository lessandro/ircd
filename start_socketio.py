#!/usr/bin/env python

import logging
import tornado.ioloop
from servers.sioserver import SioServer
import config

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    server = SioServer(config)
    tornado.ioloop.IOLoop.instance().start()
