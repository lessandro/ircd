from testutil import *


def test_privmsg(k1):
    msg('JOIN #a')
    assert code() == 'JOIN'
    while pop():
        pass

    user(2)

    msg('JOIN #a', 2)
    assert code() == 'JOIN'
    while pop():
        pass

    msg('PRIVMSG #a abc')
    assert pop() == 'test:__2 :test1!test1@::1 PRIVMSG #a abc\r\n'

    raw('connect test:__3 ::3')
    msg('PRIVMSG #a zxc', 3)
    assert code() == '451'  # not registered

    msg('PRIVMSG #b qwe')
    assert code() == '403'  # no such channel

    msg('PRIVMSG #a')
    assert code() == '461'  # not enough params

    msg('PART #a')
    assert code() == 'PART'

    msg('PRIVMSG #a test test')
    assert code() == '442'  # not on channel
