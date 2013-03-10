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


@pytest.fixture
def k1():
    r.flushdb()
    k = Kernel(Config())
    k.process_message('connect test:__1 ::1')
    k.process_message('message test:__1 USER test')
    k.process_message('message test:__1 NICK test')
    pop()
    return k


def msg(k, message):
    k.process_message('message test:__1 %s' % message)


def pop():
    return r.lpop('mq:test')


def code(reply=None):
    reply = reply or pop()
    return reply and reply.split(' ', 3)[2]
