import re
from command import command

nick_re = re.compile(ur'^\w{3,}$', re.UNICODE)
user_re = re.compile(r'^[a-zA-Z0-9_~]+$')
max_nick_len = 10  # unicode chars
max_user_len = 10


@command
def cmd_nick(server, user, nick):
    if user['nick'] != '*':
        server.send_raw(user, '999', ':You may not change your nick')
        return

    nick_utf8 = nick.decode('utf-8')[:max_nick_len]

    if not nick_re.match(nick_utf8):
        server.send_raw(user, '999', ':Invalid nick')
        return

    user['nick'] = nick
    server.save_user(user)
    check_auth(server, user)


@command
def cmd_user(server, user, username, hostname, servername, realname):
    username = username[:max_user_len]

    if not user_re.match(username):
        server.send_raw(user, '999', ':Invalid username')
        return

    if 'username' in user:
        server.send_raw(user, '462', ':You may not reregister')

    user['username'] = username
    server.save_user(user)
    check_auth(server, user)


def check_auth(server, user):
    if 'auth' in user:
        return

    if 'username' not in user:
        return

    if user['nick'] == '*':
        return

    user['auth'] = True
    user['id'] = '%s!%s@%s' % (user['nick'], user['username'], user['ip'])
    server.save_user(user)
    server.send_raw(user, '001', ':Welcome')
