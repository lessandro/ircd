import re
from command import command, is_op
from ..common.util import decolon
import irc_access

chan_re = re.compile(r'^#\w+$')


def join_chan(server, user, chan_name):
    if not chan_re.match(chan_name):
        server.send_reply(user, 'ERR_BADCHANNAME', chan_name)
        return

    chan, created = server.find_or_create_chan(chan_name)
    if server.nick_in_chan(user, chan):
        server.send_reply(user, 'ERR_ALREADYONCHANNEL', chan_name)
        return

    if created:
        server.access_list_add(chan, 'OWNER', user['id'], 0, user, '')

    mode = irc_access.check_user_access(server, chan, user)
    if mode == 'b':
        server.send_reply(user, 'ERR_BANNEDFROMCHAN', chan_name)
        return

    data = {
        'modes': mode,
        'tag': user['tag']
    }
    server.join_chan(user, chan, data)

    away = 'G' if user.get('away') else 'H'
    tag = ':%s %s' % (away, user['realname'])
    server.send_chan(user, 'JOIN', chan, tag)

    if mode:
        server.send_chan(
            user, 'MODE', chan, '+%s %s' % (mode, user['nick']),
            others_only=True)

    send_topic(server, user, chan)
    send_names(server, user, chan)


@command(auth=True, args=1)
def cmd_join(server, user, chanlist):
    chans = chanlist.split(',')
    for chan_name in chans:
        join_chan(server, user, chan_name)


def map_mode(mode):
    symbol = ''
    if 'q' in mode:
        symbol += '.'
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

    user_data = server.chan_nick(chan, user['nick'])
    if not is_op(user_data):
        server.send_reply(user, 'ERR_CHANOPRIVSNEEDED', chan['name'])
        return

    chan['topic'] = decolon(topic)
    server.save_chan(chan)
    server.send_chan(user, 'TOPIC', chan, ':%s' % chan['topic'])


@command(chan=True)
def cmd_who(server, user, chan):
    for nick, data in server.chan_nicks(chan):
        target = server.load_user(data['tag'])

        away = 'G' if user.get('away') else 'H'
        mode_sym = map_mode(data['modes']) or '*'

        server.send_reply(
            user, 'RPL_WHOREPLY', chan['name'], target['username'],
            target['ip'], server.name, target['nick'], away,
            mode_sym, '0', target['realname'])

    server.send_reply(user, 'RPL_ENDOFWHO', chan['name'])
