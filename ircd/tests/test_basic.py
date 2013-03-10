from testutil import *


def test_ping(k1):
    msg(k1, "PING abc")
    assert pop().split()[2:] == ['PONG', 'test', 'abc']


def test_quit(k1):
    msg(k1, "QUIT bye")
    assert pop() == 'test:__1 '


def test_unknown(k1):
    msg(k1, "UNKNOWNCOMMAND a b c")
    assert code() == '421'
