import collections
import logging
import time
import tornado
import tornadoredis


@tornado.gen.engine
def new_redis(callback=None):
    while True:
        try:
            logging.info('Establishing redis connection')
            redis = tornadoredis.Client()
            redis.connect()
            callback(redis)
            break
        except:
            loop = tornado.ioloop.IOLoop.instance()
            yield tornado.gen.Task(loop.add_timeout, time.time() + 1)


class RedisMQ(object):
    def __init__(self, name):
        self.name = name
        self.queue = collections.deque()

    @tornado.gen.engine
    def connect(self, callback=None):
        self.redis = None
        self.redis = yield tornado.gen.Task(new_redis)
        while self.queue:
            message = self.queue.popleft()
            self.send(message)
        callback()

    def send(self, message):
        try:
            self.redis.rpush(self.name, message)
            print '->', repr(message)
        except:
            self.queue.append(message)
            if self.redis is not None:
                self.connect()

    @tornado.gen.engine
    def loop(self, handler):
        while True:
            response = yield tornado.gen.Task(self.redis.blpop, self.name)
            if isinstance(response, Exception):
                yield tornado.gen.Task(self.connect)
            else:
                message = response[self.name]
                print '<-', repr(message)
                handler(message)
