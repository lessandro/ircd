import time
from testutil import *


def test_access(k1):
    msg('JOIN #a')
    popall()

    msg('ACCESS #a LIST')
    assert code() == '803'
    assert code() == '804'
    assert code() == '805'

    msg('ACCESS #a ADD OWNER *!zxc 123 the reasons')
    assert pop() == (
        'test:__1 :testserver 801 test1 #a OWNER *!zxc@* 122 ' +
        'test1!test1@::1 :the reasons\r\n')

    msg('ACCESS #a ADD HOST test2')
    assert code() == '801'

    msg('ACCESS #a ADD VOICE test2')
    assert code() == '801'

    user(2)
    msg('JOIN #a', 2)
    popall()

    msg('ACCESS #a DELETE HOST test2!*', 2)
    assert code() == '802'

    msg('ACCESS #a ADD OWNER *!test3@*', 2)
    assert code() == '913'

    msg('ACCESS #a DELETE OWNER test1!test1@::1', 2)
    assert code() == '913'

    msg('ACCESS #a CLEAR OWNER', 2)
    assert code() == '913'

    msg('ACCESS #a CLEAR VOICE', 2)
    assert code() == '820'

    msg('ACCESS #a LIST VOICE', 2)
    assert code() == '803'
    assert code() == '805'

    msg('ACCESS #a CLEAR', 2)
    assert code() == '820'

    msg('ACCESS #a LIST', 2)
    assert code() == '803'
    assert code() == '804'
    assert code() == '804'
    assert code() == '805'

    msg('ACCESS #a ADD DENY *')
    assert code() == '801'

    msg('PART #a')
    msg('JOIN #a')
    popall()

    msg('ACCESS #a ADD GRANT test2')
    msg('ACCESS #a ADD VOICE test3')
    assert code() == '801'

    msg('PART #a', 2)
    popall()

    msg('JOIN #a', 2)
    assert code() == 'JOIN'
    popall()

    user(3)
    user(4)
    popall()

    msg('JOIN #a', 3)
    assert code() == 'JOIN'
    assert pop() == 'test:__1,test:__2 :test3!test3@::3 MODE #a +v test3\r\n'
    popall()

    msg('JOIN #a', 4)
    assert code() == '474'  # banned


def test_access_errors(k1):
    msg('JOIN #a')
    popall()

    msg('ACCESS #a zxc')
    assert code() == '900'  # bad command

    msg('ACCESS #a ADD zx czxc')
    assert code() == '903'  # bad level

    msg('ACCESS #a add')
    assert code() == '461'  # need more params

    msg('ACCESS #a add voice')
    assert code() == '461'  # need more params

    msg('MODE #a -q test1')
    popall()

    msg('ACCESS #a ADD GRANT *')
    assert code() == '482'  # need chanop


def test_access_timeout(k1):
    msg('JOIN #a')
    popall()

    old_time = time.time
    set_time(1)

    msg('ACCESS #a ADD GRANT * 15')
    assert code() == '801'

    msg('ACCESS #a LIST GRANT')
    assert (code(), code(), code()) == ('803', '804', '805')

    set_time(10 * 60)

    msg('ACCESS #a LIST GRANT')
    assert (code(), code(), code()) == ('803', '804', '805')

    set_time(20 * 60)

    msg('ACCESS #a LIST GRANT')
    assert (code(), code()) == ('803', '805')

    time.time = old_time


def test_access_clear(k1):
    msg('JOIN #a')
    popall()

    msg('ACCESS #a ADD GRANT *')
    assert code() == '801'

    msg('PART #a')
    msg('JOIN #a')
    popall()

    msg('ACCESS #a LIST GRANT')
    assert (code(), code()) == ('803', '805')


def test_access_limit(k1):
    msg('JOIN #a')

    for i in range(10):
        msg('ACCESS #a ADD GRANT a' + str(i))

    popall()

    msg('ACCESS #a ADD GRANT a11')
    assert code() == '916'
