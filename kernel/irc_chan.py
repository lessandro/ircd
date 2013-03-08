import re
from command import command

chan_re = re.compile(r'^#\w+$')


@command
def cmd_join(server, user, chan_name):
    if not chan_re.match(chan_name):
        server.send_raw(user, '999', ':Invalid channel name')
        return

    if 'auth' not in user:
        server.send_raw(user, '451', ':You have not registered')
        return

    chan = server.find_or_create_chan(chan_name)
    if server.user_in_chan(user, chan):
        server.send_raw(user, '999', ':Already there')
        return

    server.join_chan(user, chan)
    server.send_chan(user, chan, 'JOIN')


@command
def cmd_part(server, user, chan_name):
    chan = server.find_chan(chan_name)
    if not chan:
        server.send_raw(user, '403', '%s :No such channel' % chan_name)
        return

    if not server.user_in_chan(user, chan):
        server.send_raw(
            user, '442', '%s :You\'re not on that channel' % chan['name'])
        return

    server.send_chan(user, chan, 'PART')
    server.part_chan(user, chan)
    if not server.chan_count(chan):
        server.destroy_chan(chan)
