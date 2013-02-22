import logging
import tornado
import tornadoredis


def new_redis(io_loop):
    redis = tornadoredis.Client(io_loop=io_loop)
    redis.connect()
    return redis


@tornado.gen.engine
def init_redis(io_loop, handler, callback):
    logging.info('Starting redis connections')
    redis_in = new_redis(io_loop)
    redis_out = new_redis(io_loop)
    yield tornado.gen.Task(redis_out.subscribe, 'output')
    redis_out.listen(handler)
    callback(redis_in, redis_out)
