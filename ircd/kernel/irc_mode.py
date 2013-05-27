from command import command
from ..common.util import split


@command(auth=True, args=2)
def cmd_mode(server, user, target, mode):
    if target[0] == '#':
        chan = server.find_chan(target)
        if not chan:
            server.send_reply(user, 'ERR_NOSUCHCHANNEL', target)
            return

        own_modes = server.chan_nick(chan, user['nick'])
        if not own_modes or 'o' not in own_modes:
            server.send_reply(user, 'ERR_CHANOPRIVSNEEDED', chan['name'])
            return

        chars, rest = split(mode, 1)
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

                target_modes = server.chan_nick(chan, target)
                if target_modes is None:
                    server.send_reply(
                        user, 'ERR_USERNOTINCHANNEL', target, chan['name'])
                    continue

                # check if it's necessary to add or remove the mode
                if not ((c in target_modes) ^ adding):
                    continue

                if adding:
                    target_modes += c
                else:
                    target_modes = target_modes.replace(c, '')

                server.set_chan_nick_modes(chan, target, target_modes)

                args = '%s%s %s' % ('+' if adding else '-', c, target)
                server.send_chan(user, 'MODE', chan, args)

            else:
                server.send_reply(user, 'ERR_UNKNOWNMODE', c)
    else:
        # user mode
        pass
