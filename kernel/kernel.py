import collections
import simplejson as json
import logging
import command
import redis
import replies


class Kernel(object):
    def __init__(self, config):
        self.name = config.server_name

        command.load_commands()
        self.redis = redis.StrictRedis()

    def loop(self):
        logging.info('IRCd started')

        while True:
            _, message = self.redis.blpop('mq:kernel')

            kind, origin, data = message.split(' ', 2)

            if kind == 'message':
                self.user_message(origin, data)

            elif kind == 'connect':
                self.user_connect(origin, data)

            elif kind == 'disconnect':
                self.user_disconnect(origin, data)

            elif kind == 'reset':
                self.server_reset(origin)

    def user_message(self, tag, message):
        logging.debug('message %s %s', tag, message)

        user = self.load_user(tag)
        if not user:
            logging.error('user %s not found' % tag)
            return

        try:
            message.decode('utf-8')
        except:
            self.send_reply(user, 'ERR_NONUTF8')
            return

        cmd = command.dispatch(self, user, message)
        if cmd:
            self.send_reply(user, 'ERR_UNKNOWNCOMMAND', cmd)

    def user_connect(self, tag, address):
        logging.debug('connect %s %s', tag, address)

        user = {
            'ip': address,
            'tag': tag,
            'nick': '*'
        }
        self.save_user(user)

        prefix = tag.split(':', 1)[0]
        self.redis.sadd('server-users:' + prefix, tag)

    def user_disconnect(self, tag, reason):
        logging.debug('disconnect %s %s', tag, reason)

        user = self.load_user(tag)
        if not user:
            logging.error('user %s not found' % tag)
            return

        chans = self.user_chans(user)
        for chan_name in chans:
            command.dispatch(self, user, 'PART %s' % chan_name)

        self.redis.delete('user:' + tag)

        prefix = tag[:3]
        self.redis.srem('server-users:' + prefix, tag)

    def server_reset(self, prefix):
        logging.debug('reset %s', prefix)

        tags = self.redis.smembers('server-users:' + prefix)
        for tag in tags:
            self.user_disconnect(tag, 'server reset')

    def send_chan(self, user, command, chan, args=''):
        tags = self.redis.smembers('chan-users:' + chan['name'])
        self.send(tags, ':%s %s %s %s' % (
            user['id'], command, chan['name'], args))

    def send_chan_others(self, user, command, chan, args=''):
        tags = self.redis.smembers('chan-users:' + chan['name'])
        tags.remove(user['tag'])
        self.send(tags, ':%s %s %s %s' % (
            user['id'], command, chan['name'], args))

    def send_reply(self, target, reply, *args):
        numeric, format = replies.replies[reply]
        self.send(target['tag'], ':%s %s %s %s' % (
            self.name, numeric, target['nick'], format % args))

    def send_raw(self, target, raw, args):
        self.send(target['tag'], ':%s %s %s %s' % (
            self.name, raw, target['nick'], args))

    def send(self, tags, message):
        if type(tags) is str:
            prefix = tags.split(':', 1)[0]
            self.redis.rpush('mq:' + prefix, '%s %s\r\n' % (tags, message))
            return

        prefixes = collections.defaultdict(list)
        for tag in tags:
            prefixes[tag.split(':', 1)[0]].append(tag)

        for prefix, tags in prefixes.iteritems():
            tags = ','.join(tags)
            self.redis.rpush('mq:' + prefix, '%s %s\r\n' % (tags, message))

    def disconnect(self, user):
        tag = user['tag']
        self.redis.rpush('mq:' + tag.split(':', 1)[0], '%s ' % tag)

    def load_user(self, tag):
        serialized = self.redis.get('user:' + tag)
        return serialized and json.loads(serialized)

    def save_user(self, user):
        serialized = json.dumps(user)
        self.redis.set('user:' + user['tag'], serialized)

    def find_or_create_chan(self, chan_name):
        chan = self.find_chan(chan_name)
        if chan:
            return chan

        chan = {
            'name': chan_name
        }
        self.save_chan(chan)
        return chan

    def find_chan(self, chan_name):
        chan = self.redis.get('chan:' + chan_name)
        return chan and json.loads(chan)

    def save_chan(self, chan):
        serialized = json.dumps(chan)
        chan = self.redis.set('chan:' + chan['name'], serialized)

    def join_chan(self, user, chan):
        self.redis.sadd('chan-users:' + chan['name'], user['tag'])
        self.redis.sadd('chan-nicks:' + chan['name'], user['nick'])
        self.redis.sadd('user-chans:' + user['tag'], chan['name'])

    def part_chan(self, user, chan):
        self.redis.srem('chan-users:' + chan['name'], user['tag'])
        self.redis.srem('chan-nicks:' + chan['name'], user['nick'])
        self.redis.srem('user-chans:' + user['tag'], chan['name'])

    def user_in_chan(self, user, chan):
        return self.redis.sismember('chan-nicks:' + chan['name'], user['nick'])

    def user_chans(self, user):
        return self.redis.smembers('user-chans:' + user['tag'])

    def chan_count(self, chan):
        return self.redis.scard('chan-nicks:' + chan['name'])

    def destroy_chan(self, chan):
        self.redis.delete('chan:' + chan['name'])
