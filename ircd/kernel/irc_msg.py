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

        server.send_chan(user, 'PRIVMSG', chan, message, others_only=True)
    else:
        tags = server.find_nick(target)
        if not tags:
            server.send_reply(user, 'ERR_NOSUCHNICK', target)
            return

        server.send_command(tags, user, 'PRIVMSG', target, message)
