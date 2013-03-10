from command import command


@command
def cmd_privmsg(server, user, target, message):
    if 'auth' not in user:
        server.send_reply(user, 'ERR_NOTREGISTERED')
        return

    if not target or not message:
        server.send_reply(user, 'ERR_NEEDMOREPARAMS', 'PRIVMSG')
        return

    if target[0] == '#':
        chan = server.find_chan(target)
        if not chan:
            server.send_reply(user, 'ERR_NOSUCHCHANNEL', target)
            return

        if not server.user_in_chan(user, chan):
            server.send_reply(user, 'ERR_NOTONCHANNEL', target)
            return

        server.send_chan_others(user, 'PRIVMSG', chan, message)
    else:
        print 'PRIVMSG user'
