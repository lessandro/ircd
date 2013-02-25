from command import command


@command
def cmd_user(server, user, username, hostname, servername, realname):
    print 'USER', username, hostname, servername, realname
    server.send(user, ':server 001 nick :welcome')


@command
def cmd_nick(server, user, nick):
    print 'NICK', nick


@command
def cmd_quit(server, user, message):
    print 'QUIT', message
    server.disconnect(user)


@command
def cmd_join(server, user, chan):
    print 'JOIN', chan


@command
def cmd_part(server, user, chan):
    print 'PART', chan
