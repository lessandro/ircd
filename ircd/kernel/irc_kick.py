from command import command
from ..common.util import colon


@command(chan=True, args=2)
def cmd_kick(server, user, chan, target, message):
    own_data = server.chan_nick(chan, user['nick'])
    if not own_data or 'o' not in own_data['modes']:
        server.send_reply(user, 'ERR_CHANOPRIVSNEEDED', chan['name'])
        return

    target_data = server.chan_nick(chan, target)
    if not target_data:
        server.send_reply(user, 'ERR_USERNOTINCHANNEL', target, chan['name'])
        return

    # ok to kick
    server.send_chan(user, 'KICK', chan, '%s %s' % (target, colon(message)))

    target_user = server.load_user(target_data['tag'])
    server.part_chan(target_user, chan)
