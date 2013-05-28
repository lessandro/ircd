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
    msg('MODE #a -o test1')
    popall()
    msg('KICK #a test1')
    assert code() == '482'  # not op
