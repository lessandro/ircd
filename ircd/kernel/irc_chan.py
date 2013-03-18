import re
from command import command

chan_re = re.compile(r'^#\w+$')


@command(auth=True, args=1)
def cmd_join(server, user, chan_name):
    if not chan_re.match(chan_name):
        server.send_reply(user, 'ERR_BADCHANNAME', chan_name)
        return

    chan, created = server.find_or_create_chan(chan_name)
    if server.nick_in_chan(user, chan):
        server.send_reply(user, 'ERR_ALREADYONCHANNEL', chan_name)
        return

    server.join_chan(user, chan, 'o' if created else '')
    server.send_chan(user, 'JOIN', chan)

    if chan['topic']:
        server.send_reply(user, 'RPL_TOPIC', chan['name'], chan['topic'])
    else:
        server.send_reply(user, 'RPL_NOTOPIC', chan['name'])

    send_names(server, user, chan)


def map_mode(mode):
    if 'o' in mode:
        return '@'
    return ''


def send_names(server, user, chan):
    nicks = []
    for nick, mode in server.chan_nicks(chan).iteritems():
        nicks.append('%s%s' % (map_mode(mode), nick))
    nick_list = ' '.join(nicks)

    server.send_reply(user, 'RPL_NAMREPLY', chan['name'], nick_list)
    server.send_reply(user, 'RPL_ENDOFNAMES', chan['name'])


@command(chan=True)
def irc_names(server, user, chan):
    send_names(server, user, chan)


@command(chan=True)
def cmd_part(server, user, chan):
    server.send_chan(user, 'PART', chan)
    server.part_chan(user, chan)
    if not server.chan_count(chan):
        server.destroy_chan(chan)
