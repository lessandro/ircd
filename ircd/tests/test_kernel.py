from testutil import *


def test_reset(k1):
    msg('JOIN #a')
    while pop():
        pass

    raw('reset test ')
    assert pop() == 'test:__1 :test1!test1@::1 PART #a\r\n'


def test_utf8(k1):
    msg('PING \xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA')
    assert code() == '903'  # invalid utf8


def test_nouser(k0):
    msg('PING oi')
    assert code() is None

    raw('disconnect test:__1 ')
    assert code() is None
