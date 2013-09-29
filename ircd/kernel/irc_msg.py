from command import command, is_op
from ..common.util import colon


def send_message(kind, server, user, target, message):
    message = colon(message)

    if target[0] == '#':
        chan = server.find_chan(target)
        if not chan:
            server.send_reply(user, 'ERR_NOSUCHCHANNEL', target)
            return

        # it's actually ok to send a message across connections if both
        # are authenticated and with the same nick
        user_data = server.chan_nick(chan, user['nick'])
        if not user_data:
            server.send_reply(user, 'ERR_NOTONCHANNEL', target)
            return

        if 'm' in chan['modes']:
            modes = user_data['modes']
            can_talk = is_op(user_data) or 'v' in modes
            if not can_talk:
                server.send_reply(user, 'ERR_CANNOTSENDTOCHAN', chan['name'])
                return

        server.send_chan(user, kind, chan, message, others_only=True)
    else:
        tags = server.find_nick(target)
        if not tags:
            server.send_reply(user, 'ERR_NOSUCHNICK', target)
            return

        server.send_command(tags, user, kind, target, message)


@command(auth=True, args=2)
def cmd_privmsg(server, user, target, message):
    send_message('PRIVMSG', server, user, target, message)


@command(auth=True, args=2)
def cmd_notice(server, user, target, message):
    send_message('NOTICE', server, user, target, message)


@command(auth=True, args=3)
def cmd_whisper(server, user, chan, target, message):
    send_message('PRIVMSG', server, user, target, message)
