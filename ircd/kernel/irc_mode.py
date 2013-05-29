from command import command
from ..common.util import split


def mode_chan(server, user, target, args):
    chan = server.find_chan(target)
    if not chan:
        server.send_reply(user, 'ERR_NOSUCHCHANNEL', target)
        return

    own_data = server.chan_nick(chan, user['nick'])
    if not own_data or 'o' not in own_data['modes']:
        server.send_reply(user, 'ERR_CHANOPRIVSNEEDED', chan['name'])
        return

    chars, rest = split(args, 1)
    adding = True

    for c in chars:
        if c in '+-':
            adding = c == '+'

        # op/voice
        elif c in 'ov':
            target, rest = split(rest, 1)

            if not target:
                # no target supplied
                continue

            target_data = server.chan_nick(chan, target)
            if target_data is None:
                server.send_reply(
                    user, 'ERR_USERNOTINCHANNEL', target, chan['name'])
                continue

            target_modes = target_data['modes']

            # check if it's necessary to add or remove the mode
            if not ((c in target_modes) ^ adding):
                continue

            if adding:
                target_modes += c
            else:
                target_modes = target_modes.replace(c, '')

            target_data['modes'] = target_modes
            server.set_chan_nick(chan, target, target_data)

            args = '%s%s %s' % ('+' if adding else '-', c, target)
            server.send_chan(user, 'MODE', chan, args)

        else:
            server.send_reply(user, 'ERR_UNKNOWNMODE', c)


@command(auth=True, args=1)
def cmd_mode(server, user, target, args):
    if target[0] == '#':
        mode_chan(server, user, target, args)
    else:
        # user mode
        pass
