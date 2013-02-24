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


class RedisSub(object):
    def __init__(self, channel, handler):
        self.handler = handler
        self.channel = channel
        self.reconnect()

    @tornado.gen.engine
    def reconnect(self):
        self.redis = None
        self.redis = yield tornado.gen.Task(new_redis)
        yield tornado.gen.Task(self.redis.subscribe, self.channel)
        self.redis.listen(self.handle_message)

    def handle_message(self, message):
        if message is None:
            self.reconnect()
        elif message.kind == 'message':
            self.handler(message.body)
            print '<-', repr(message.body)


class RedisMQ(object):
    def __init__(self, name):
        self.name = name
        self.queue = collections.deque()
        self.reconnect()

    @tornado.gen.engine
    def reconnect(self):
        self.redis = None
        self.redis = yield tornado.gen.Task(new_redis)
        while self.queue:
            message = self.queue.popleft()
            self.send(message)

    def send(self, message):
        try:
            self.redis.rpush(self.name, message)
            print '->', repr(message)
        except:
            self.queue.append(message)
            if self.redis is not None:
                self.reconnect()
