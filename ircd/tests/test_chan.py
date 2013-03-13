from testutil import *


def test_join1(k0):
    raw('connect test:__1 ::1')

    msg('JOIN #a')
    assert code() == '451'  # not registered

    msg('JOIN #!')
    assert code() == '479'  # invalid channel name


def test_join2(k1):
    msg('JOIN #a')
    assert pop().split()[2:] == ['JOIN', '#a']

    msg('JOIN #a')
    assert code() == '901'  # already joined


def test_join3(k1):
    msg('JOIN #a')
    pop()

    raw('connect test:__2 ::2')
    msg('NICK test1', 2)
    msg('USER test1', 2)
    assert code() == '001'

    msg('JOIN #a', 2)
    assert code() == '901'  # already joined


def test_part1(k1):
    msg('PART #a')
    assert code() == '403'  # no such channel

    user(2)

    msg('JOIN #a', 2)
    pop()

    msg('PART #a')
    assert code() == '442'  # not on chan

    msg('PART #a', 2)
    assert pop() == 'test:__2 :test2!test2@::2 PART #a\r\n'


def test_part2(k1):
    msg('JOIN #a')
    pop()

    msg('JOIN #b')
    pop()

    user(2)
    msg('JOIN #a', 2)
    pop()

    raw('disconnect test:__1 reason')
    assert pop() == 'test:__1 :test1!test1@::1 PART #b\r\n'
