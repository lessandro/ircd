from command import command


@command
def cmd_join(server, user, chan):
    print 'JOIN', chan


@command
def cmd_part(server, user, chan):
    print 'PART', chan
