import time
from testutil import *


def test_timeout():
    old_time = time.time
    set_time(0)

    k = k1()  # 10 second ping timeout

    k.timeout.check()
    assert not pop()

    set_time(11)
    k.timeout.check()
    # send ping after 10 seconds of inactivity
    assert pop() == 'test:__1 PING :testserver\r\n'

    set_time(12)
    msg('PONG x')

    set_time(13)
    k.timeout.check()
    assert not pop()

    set_time(24)
    k.timeout.check()
    assert pop() == 'test:__1 PING :testserver\r\n'

    set_time(35)
    k.timeout.check()
    # disconnect user
    assert pop() == 'test:__1 '

    time.time = old_time


def test_timeout2():
    old_time = time.time
    set_time(0)

    k = k1()  # 10 second ping timeout

    k.timeout.check()
    assert not pop()

    raw('disconnect test:__1 ')

    set_time(11)
    k.timeout.check()
    # should not send a ping message to someone who disconnected
    assert not pop()

    time.time = old_time
