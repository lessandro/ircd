from testutil import *


def test_kick(k1):
    msg('JOIN #b')
    popall()

    msg('KICK #a')
    assert code() == '461'  # not enough params

    msg('KICK #a nick')
    assert code() == '403'  # no such channel

    msg('JOIN #a')
    popall()

    msg('KICK #a nick')
    assert code() == '441'  # target not in chan

    # kick self
    msg('KICK #a test1')
    assert code() == 'KICK'

    msg('JOIN #a')
    msg('MODE #a -q test1')
    popall()
    msg('KICK #a test1')
    assert code() == '482'  # not op


def test_kick_owner(k1):
    user(2)
    msg('JOIN #a')
    msg('JOIN #a', 2)
    msg('MODE #a +o test2')
    popall()

    msg('KICK #a test1', 2)
    assert code() == '482'
