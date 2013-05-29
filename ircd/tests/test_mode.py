from testutil import *


def test_mode_chan(k1):
    msg('JOIN #a')
    user(2)
    msg('JOIN #a', 2)
    msg('JOIN #b', 2)

    popall()

    msg('MODE #c +o test')
    assert code() == '403'  # no such channel

    # not in channel
    msg('MODE #b +o test')
    assert code() == '482'  # not chan op

    msg('MODE #a +o test9')
    assert code() == '441'  # target not in chan

    # in channel, not op
    msg('MODE #a +o test2', 2)
    assert code() == '482'  # not chan op

    msg('MODE #a +y test1')
    assert code() == '472'  # unknown mode

    msg('MODE #a +o test2')
    assert pop() == 'test:__1,test:__2 :test1!test1@::1 MODE #a +o test2\r\n'

    # already op
    msg('MODE #a +o test2')
    assert not pop()

    msg('MODE #a +v test2', 2)
    assert pop() == 'test:__1,test:__2 :test2!test2@::2 MODE #a +v test2\r\n'

    msg('MODE #a -o test2', 2)
    assert pop() == 'test:__1,test:__2 :test2!test2@::2 MODE #a -o test2\r\n'

    user(3)
    popall()

    msg('JOIN #a', 3)
    pop()  # JOIN
    pop()  # topic
    names = pop().strip().split(':')[3].split(' ')
    assert '@test1' in names
    assert '+test2' in names
    assert 'test3' in names
    pop()  # end of names

    msg('MODE #a +vv-v+v test1 test3 test3')
    assert code() == 'MODE'
    assert code() == 'MODE'
    assert code() == 'MODE'
    assert not pop()  # no target supplied for last +v


def test_mode_chan2(k1):
    msg('JOIN #a')
    popall()

    msg('MODE #a')
    assert pop() == 'test:__1 :testserver 324 test1 #a +\r\n'

    msg('MODE #a +m')
    assert pop() == 'test:__1 :test1!test1@::1 MODE #a +m\r\n'

    msg('MODE #a +m')
    assert not pop()

    msg('MODE #a')
    assert pop() == 'test:__1 :testserver 324 test1 #a +m\r\n'

    msg('MODE #a -m')
    assert pop() == 'test:__1 :test1!test1@::1 MODE #a -m\r\n'

    msg('MODE #a')
    assert pop() == 'test:__1 :testserver 324 test1 #a +\r\n'
