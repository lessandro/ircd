import hmac
import hashlib
import msgpack
import time
import re
from command import command

nick_re = re.compile(ur'^\w{3,}$', re.UNICODE)
user_re = re.compile(r'^[a-zA-Z0-9_~]+$')
max_nick_len = 10  # unicode chars
max_user_len = 10


def validate_nick(server, user, nick):
    nick_utf8 = nick.decode('utf-8')[:max_nick_len]

    if not nick_re.match(nick_utf8):
        server.send_reply(user, 'ERR_ERRONEOUSNICKNAME', nick)
        return False

    return nick_utf8.encode('utf-8')


@command(args=1)
def cmd_nick(server, user, nick):
    if user['nick'] != '*':
        server.send_reply(user, 'ERR_ALREADYREGISTRED')
        return

    nick = validate_nick(server, user, nick)

    if not nick:
        return

    user['nick'] = nick
    server.save_user(user)
    check_auth(server, user)


def validate_username(server, user, username):
    username = username[:max_user_len]

    if not user_re.match(username):
        server.send_reply(user, 'ERR_ERRONEOUSUSERNAME', username)
        return False

    return username


@command(args=1)
def cmd_user(server, user, username, hostname, servername, realname):
    if 'username' in user:
        server.send_reply(user, 'ERR_ALREADYREGISTRED')
        return

    username = validate_username(server, user, username)

    if not username:
        return

    user['username'] = username
    server.save_user(user)
    check_auth(server, user)


@command(args=2)
def cmd_auth(server, user, hex_data, hex_digest):
    if 'auth' in user:
        server.send_reply(user, 'ERR_ALREADYREGISTRED')
        return

    try:
        h = hmac.new(server.config.hmac_key, hex_data, hashlib.sha256)
        if hex_digest != h.hexdigest():
            server.send_reply(user, 'ERR_AUTHERROR', 'digest mismatch')
            return

        data = msgpack.loads(hex_data.decode('hex'))

        if data['expires'] < time.time():
            server.send_reply(user, 'ERR_AUTHERROR', 'expired token')
            return

        nick = validate_nick(server, user, data['nick'])
        username = validate_username(server, user, data['username'])

        if not nick or not username:
            return

        user['nick'] = nick
        user['username'] = username

        check_auth(server, user)

    except:
        server.send_reply(user, 'ERR_AUTHERROR', 'malformed data')
        return


@command
def cmd_login(server, user, username, nick):
    data = {
        'username': username,
        'nick': nick,
        'expires': time.time() + 60
    }

    hex_data = msgpack.dumps(data).encode('hex')
    h = hmac.new(server.config.hmac_key, hex_data, hashlib.sha256)
    command.dispatch(server, user, 'AUTH %s %s' % (hex_data, h.hexdigest()))


def check_auth(server, user):
    if 'auth' in user:
        # this should never be executed
        return

    if 'username' not in user:
        return

    if user['nick'] == '*':
        return

    user['auth'] = True
    user['id'] = '%s!%s@%s' % (user['nick'], user['username'], user['ip'])
    server.save_user(user)
    server.register_nick(user)
    server.send_reply(user, 'RPL_WELCOME')
    server.send_reply(user, 'RPL_MYINFO')
    server.send_reply(user, 'RPL_ISUPPORT')
