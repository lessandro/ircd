from command import command, is_op
from ..common.util import colon


@command(chan=True, args=2)
def cmd_kick(server, user, chan, target, message):
    user_data = server.chan_nick(chan, user['nick'])
    if not is_op(user_data):
        server.send_reply(user, 'ERR_CHANOPRIVSNEEDED', chan['name'])
        return

    target_data = server.chan_nick(chan, target)
    if not target_data:
        server.send_reply(user, 'ERR_USERNOTINCHANNEL', target, chan['name'])
        return

    # +o can't kick +q
    if 'q' not in user_data['modes'] and 'q' in target_data['modes']:
        server.send_reply(user, 'ERR_CHANOPRIVSNEEDED', chan['name'])
        return

    # ok to kick
    server.send_chan(user, 'KICK', chan, '%s %s' % (target, colon(message)))

    target_user = server.load_user(target_data['tag'])
    server.part_chan(target_user, chan)
