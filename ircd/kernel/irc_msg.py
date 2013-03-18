from command import command


@command(auth=True, args=2)
def cmd_privmsg(server, user, target, message):
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
