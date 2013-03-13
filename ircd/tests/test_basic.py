from testutil import *


def test_ping(k1):
    msg("PING abc")
    assert pop() == 'test:__1 :testserver PONG test1 abc\r\n'


def test_quit(k1):
    msg("QUIT bye")
    assert pop() == 'test:__1 '


def test_unknown(k1):
    msg("UNKNOWNCOMMAND a b c")
    assert code() == '421'  # unknown command
