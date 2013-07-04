from testutil import *


def test_join1(k0):
    raw('connect test:__1 ::1')

    msg('JOIN #a')
    assert code() == '451'  # not registered

    msg('nick test')
    msg('user test')
    popall()

    msg('JOIN #!')
    assert code() == '479'  # invalid channel name


def test_join2(k1):
    msg('JOIN #a')
    assert pop().split()[2:] == ['JOIN', '#a', ':real' ,'name']
    assert code() == '331'
    assert code() == '353'
    assert code() == '366'

    msg('JOIN #a')
    assert code() == '927'  # already joined


def test_join3(k1):
    msg('JOIN #a')
    popall()

    raw('connect test:__2 ::2')
    msg('NICK test1', 2)
    msg('USER test1', 2)
    assert code() == '001'
    popall()

    msg('JOIN #a', 2)
    assert code() == '927'  # already joined


def test_part1(k1):
    msg('PART #a')
    assert code() == '403'  # no such channel

    user(2)

    msg('JOIN #a', 2)
    popall()

    msg('PART #a')
    assert code() == '442'  # not on chan

    msg('PART #a', 2)
    assert pop() == 'test:__2 :test2!test2@::2 PART #a\r\n'


def test_part2(k1):
    msg('JOIN #a')
    popall()

    msg('JOIN #b')
    popall()

    user(2)
    msg('JOIN #a', 2)
    popall()

    raw('disconnect test:__1 reason')
    assert pop() == 'test:__1 :test1!test1@::1 PART #b\r\n'


def test_names(k1):
    msg('JOIN #a')
    raw('connect test:__2 ::2')
    msg('NICK test2', 2)
    msg('USER test2', 2)
    msg('JOIN #a', 2)

    popall()

    msg('NAMES #a')
    _, serv, code_, equal, nick, chan, nicks = pop().split(' ', 6)
    assert code_ == '353'
    nicks = nicks[1:].split()
    assert '.test1' in nicks
    assert 'test2' in nicks
    assert code() == '366'


def test_multiple(k1):
    msg('JOIN #a,#b')
    popall()

    msg('PRIVMSG #a :oi')
    msg('PRIVMSG #b :oi')
    assert pop() is None


def test_topic(k1):
    msg('JOIN #a')
    popall()

    msg('TOPIC #b')
    assert code() == '403'  # no such channel

    msg('TOPIC #a')
    assert code() == '331'  # no topic set

    msg('TOPIC #a abc def')
    assert pop() == 'test:__1 :test1!test1@::1 TOPIC #a :abc def\r\n'

    msg('TOPIC #a')
    assert pop() == 'test:__1 :testserver 332 test1 #a :abc def\r\n'

    msg('TOPIC #a :')
    assert pop() == 'test:__1 :test1!test1@::1 TOPIC #a :\r\n'

    msg('MODE #a -q test1')
    pop()

    msg('TOPIC #a')
    assert code() == '331'  # no topic set

    msg('topic #a :asd')
    assert code() == '482'  # not op


def test_who(k1):
    msg('JOIN #a')
    popall()

    msg('WHO #a')
    assert code() == '352'  # who reply
    assert code() == '315'  # end of who
