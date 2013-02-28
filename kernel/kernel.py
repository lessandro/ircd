import collections
import simplejson as json
import logging
import command
import redis


class Kernel(object):
    def __init__(self, config):
        self.name = config.server_name

        command.load_commands()
        self.redis = redis.StrictRedis()

    def loop(self):
        logging.info('IRCd started')

        while True:
            _, message = self.redis.blpop('mq-kernel')

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
            self.send_raw(user, '999', 'Non-utf8 data')
            return

        command.dispatch(self, user, message)

    def user_connect(self, tag, address):
        logging.debug('connect %s %s', tag, address)

        user = {
            'ip': address,
            'tag': tag,
            'nick': '*'
        }
        self.save_user(user)

        prefix = tag[:3]
        self.redis.sadd(prefix, tag)

    def user_disconnect(self, tag, reason):
        logging.debug('disconnect %s %s', tag, reason)

        self.redis.delete(tag)

        prefix = tag[:3]
        self.redis.srem(prefix, tag)

    def server_reset(self, prefix):
        logging.debug('reset %s', prefix)

        tags = self.redis.smembers(prefix)
        for tag in tags:
            self.user_disconnect(tag, 'server reset')

    def send_raw(self, target, raw, args):
        self.send(target['tag'], ':%s %s %s %s' %
            (self.name, raw, target['nick'], args))

    def send(self, tags, message):
        if type(tags) is str:
            prefix = tags[:3]
            self.redis.rpush('mq-' + prefix, '%s %s\r\n' % (tags, message))
            return

        prefixes = collections.defaultdict(list)
        for tag in tags:
            prefixes[tag[:3]].append(tag)

        for prefix, tags in prefixes.iteritems():
            tags = ','.join(tags)
            self.redis.rpush('mq-' + prefix, '%s %s\r\n' % (tags, message))

    def disconnect(self, user):
        tag = user['tag']
        self.redis.rpush('mq-' + tag[:3], '%s ' % tag)

    def load_user(self, tag):
        serialized = self.redis.get(tag)
        return serialized and json.loads(serialized)

    def save_user(self, user):
        serialized = json.dumps(user)
        self.redis.set(user['tag'], serialized)
