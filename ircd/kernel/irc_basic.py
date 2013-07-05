from command import command
from ..common.util import decolon


@command
def cmd_ping(server, user, args):
    server.send_reply(user, 'PONG', args)


@command
def cmd_pong(server, user, args):
    pass


@command
def cmd_quit(server, user, message):
    server.disconnect(user)


@command
def cmd_away(server, user, message):
    message = decolon(message)

    user['away'] = message
    server.save_user(user)

    if message:
        server.send_reply(user, 'RPL_NOWAWAY')
        server.send_visible(user, 'RPL_AWAYBROADCAST', message)
    else:
        server.send_reply(user, 'RPL_UNAWAY')
        server.send_visible(user, 'RPL_UNAWAYBROADCAST')
