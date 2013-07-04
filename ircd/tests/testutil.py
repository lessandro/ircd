import pytest
import redis
import time
from ircd.kernel.kernel import Kernel

r = redis.StrictRedis(db=1)
k = None


class Config(object):
    server_name = 'testserver'
    ping_timeout = 10
    redis_db = 1
    hmac_key = 'key'


@pytest.fixture
def k0():
    global k
    r.flushdb()
    k = Kernel(Config())
    return k


@pytest.fixture
def k1():
    k = k0()
    user(1)
    return k


def user(n=1):
    raw('connect test:__%d ::%d' % (n, n))
    msg('USER test%d hn sn :real name' % n, n)
    msg('NICK test%d' % n, n)
    popall()


def raw(message):
    k.process_message(message)


def msg(message, n=1):
    raw('message test:__%d %s' % (n, message))


def pop():
    return r.lpop('mq:test')


def popall():
    while pop():
        pass


def code(reply=None):
    reply = reply or pop()
    return reply and reply.split(' ', 3)[2]


def set_time(t):
    time.time = lambda: t
