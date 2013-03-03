import re
from command import command

nick_re = re.compile(r'^\w{3,}$')


@command
def cmd_nick(server, user, nick):
    if not nick_re.match(nick):
        server.send_raw(user, '999', ':Invalid nick')
        return

    user['nick'] = nick
    server.save_user(user)


@command
def cmd_user(server, user, username, hostname, servername, realname):
    if not nick_re.match(username):
        server.send_raw(user, '999', ':Invalid username')
        return

    if 'username' in user:
        server.send_raw(user, '462', ':You may not reregister')

    user['username'] = username
    server.save_user(user)
    check_auth(server, user)


def check_auth(server, user):
    if user['nick'] == '*':
        return

    if 'username' not in user:
        return

    if 'auth' in user:
        return

    user['auth'] = True
    server.save_user(user)
    server.send_raw(user, '001', ':Welcome')


@command
def cmd_ping(server, user, args):
    server.send_raw(user, 'PONG', args)


@command
def cmd_quit(server, user, message):
    print 'QUIT', message
    server.disconnect(user)
