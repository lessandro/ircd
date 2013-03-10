import re
from command import command

chan_re = re.compile(r'^#\w+$')


@command
def cmd_join(server, user, chan_name):
    if not chan_re.match(chan_name):
        server.send_reply(user, 'ERR_BADCHANNAME', chan_name)
        return

    if 'auth' not in user:
        server.send_reply(user, 'ERR_NOTREGISTERED')
        return

    chan = server.find_or_create_chan(chan_name)
    if server.user_in_chan(user, chan):
        server.send_reply(user, 'ERR_ALREADYONCHANNEL', chan_name)
        return

    server.join_chan(user, chan)
    server.send_chan(user, 'JOIN', chan)


@command
def cmd_part(server, user, chan_name):
    chan = server.find_chan(chan_name)
    if not chan:
        server.send_reply(user, 'ERR_NOSUCHCHANNEL', chan_name)
        return

    if not server.user_in_chan(user, chan):
        server.send_reply(user, 'ERR_NOTONCHANNEL', chan_name)
        return

    server.send_chan(user, 'PART', chan)
    server.part_chan(user, chan)
    if not server.chan_count(chan):
        server.destroy_chan(chan)
