import pytest
import redis
from ircd.kernel.kernel import Kernel

r = redis.StrictRedis(db=1)


class Config(object):
    server_name = 'testserver'
    redis_db = 1


@pytest.fixture
def k0():
    r.flushdb()
    return Kernel(Config())


def pop():
    return r.lpop('mq:test')


def code(reply=None):
    reply = reply or pop()
    return reply and reply.split(' ', 3)[2]
