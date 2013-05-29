import re
from command import command
from ..common.util import decolon

chan_re = re.compile(r'^#\w+$')


def join_chan(server, user, chan_name):
    if not chan_re.match(chan_name):
        server.send_reply(user, 'ERR_BADCHANNAME', chan_name)
        return

    chan, created = server.find_or_create_chan(chan_name)
    if server.nick_in_chan(user, chan):
        server.send_reply(user, 'ERR_ALREADYONCHANNEL', chan_name)
        return

    data = {
        'modes': 'o' if created else '',
        'tag': user['tag']
    }
    server.join_chan(user, chan, data)
    server.send_chan(user, 'JOIN', chan)

    send_topic(server, user, chan)
    send_names(server, user, chan)


@command(auth=True, args=1)
def cmd_join(server, user, chanlist):
    chans = chanlist.split(',')
    for chan_name in chans:
        join_chan(server, user, chan_name)


def map_mode(mode):
    symbol = ''
    if 'o' in mode:
        symbol += '@'
    if 'v' in mode:
        symbol += '+'
    return symbol


def send_names(server, user, chan):
    nicks = []
    for nick, data in server.chan_nicks(chan):
        nicks.append('%s%s' % (map_mode(data['modes']), nick))
    nick_list = ' '.join(nicks)

    server.send_reply(user, 'RPL_NAMREPLY', chan['name'], nick_list)
    server.send_reply(user, 'RPL_ENDOFNAMES', chan['name'])


def send_topic(server, user, chan):
    if chan['topic']:
        server.send_reply(user, 'RPL_TOPIC', chan['name'], chan['topic'])
    else:
        server.send_reply(user, 'RPL_NOTOPIC', chan['name'])


@command(chan=True)
def irc_names(server, user, chan):
    send_names(server, user, chan)


@command(chan=True)
def cmd_part(server, user, chan):
    server.send_chan(user, 'PART', chan)
    server.part_chan(user, chan)


@command(chan=True)
def cmd_topic(server, user, chan, topic):
    if not topic:
        send_topic(server, user, chan)
        return

    own_data = server.chan_nick(chan, user['nick'])
    if not own_data or 'o' not in own_data['modes']:
        server.send_reply(user, 'ERR_CHANOPRIVSNEEDED', chan['name'])
        return

    chan['topic'] = decolon(topic)
    server.save_chan(chan)
    server.send_chan(user, 'TOPIC', chan, ':%s' % chan['topic'])
