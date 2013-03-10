from command import command


@command
def cmd_ping(server, user, args):
    server.send_raw(user, 'PONG', args)


@command
def cmd_quit(server, user, message):
    server.disconnect(user)
