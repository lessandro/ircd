from testutil import *


def test_privmsg_chan(k1):
    msg('JOIN #a')
    assert code() == 'JOIN'
    popall()

    user(2)

    msg('JOIN #a', 2)
    assert code() == 'JOIN'
    popall()

    msg('PRIVMSG #a abc')
    assert pop() == 'test:__2 :test1!test1@::1 PRIVMSG #a :abc\r\n'

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


def test_privmsg_user(k1):
    user(2)

    msg('PRIVMSG test2 :hi')
    assert pop() == 'test:__2 :test1!test1@::1 PRIVMSG test2 :hi\r\n'

    msg('PRIVMSG test3 :hi3')
    assert code() == '401'

    raw('connect test:__2b ::2')
    raw('message test:__2b NICK test2')
    raw('message test:__2b USER test2')
    popall()

    msg('PRIVMSG test2 :hi2')
    tags, message = pop().split(' ', 1)
    tags = tags.split(',')
    assert len(tags) == 2
    assert 'test:__2' in tags
    assert 'test:__2b' in tags
    assert message == ':test1!test1@::1 PRIVMSG test2 :hi2\r\n'

    raw('disconnect test:__2 ')
    msg('PRIVMSG test2 :hi')
    assert pop() == 'test:__2b :test1!test1@::1 PRIVMSG test2 :hi\r\n'


def test_notice(k1):
    user(2)

    msg('NOTICE test2 hello')
    assert pop() == 'test:__2 :test1!test1@::1 NOTICE test2 :hello\r\n'
