from command import command


@command
def cmd_privmsg(server, user, target, message):
    if 'auth' not in user:
        server.send_raw(user, '451', ':You have not registered')
        return

    if not target or not message:
        server.send_raw(user, '461', 'PRIVMSG :Not enough parameters')
        return

    if target[0] == '#':
        chan = server.find_chan(target)
        if not chan:
            server.send_raw(user, '403', '%s :No such channel' % target)
            return

        if not server.user_in_chan(user, chan):
            server.send_raw(
                user, '442', '%s :You\'re not on that channel' % target)
            return

        server.send_chan_others(user, chan, 'PRIVMSG', message)
    else:
        print 'PRIVMSG user'
