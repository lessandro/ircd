from testutil import *


def test_auth_ok(k0):
    k0.process_message('connect test:__1 ::1')

    k0.process_message('message test:__1 USER test')
    k0.process_message('message test:__1 NICK test')
    assert code() == '001'
    assert code() == '004'
    assert code() == '005'

    k0.process_message('disconnect test:__1 ')
    assert pop() is None


def test_auth_fail(k0):
    k0.process_message('connect test:__1 ::1')

    k0.process_message('message test:__1 NICK test#')
    assert code() == '432'  # invalid nick

    k0.process_message('message test:__1 NICK test')
    assert pop() is None

    k0.process_message('message test:__1 NICK test')
    assert code() == '462'  # already registered

    k0.process_message('message test:__1 USER !')
    assert code() == '997'  # invalid username

    k0.process_message('message test:__1 USER test')
    assert code() == '001'
    assert code() == '004'
    assert code() == '005'

    k0.process_message('message test:__1 USER test2')
    assert code() == '462'  # already registered

    k0.process_message('disconnect test:__1 ')
    assert pop() is None
