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
            _, message = self.redis.blpop('input')

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
            decoded = message.decode('utf-8')
        except:
            self.send_raw(user, '999', 'Non-utf8 data')
            return

        command.dispatch(self, user, decoded)

    def user_connect(self, tag, address):
        logging.debug('connect %s %s', tag, address)

        user = {
            'ip': address,
            'tag': tag,
            'nick': '*'
        }
        self.save_user(user)

    def user_disconnect(self, tag, reason):
        logging.debug('disconnect %s %s', tag, reason)

        self.redis.delete(tag)

    def server_reset(self, prefix):
        logging.debug('reset %s', prefix)

    def send_raw(self, target, raw, args):
        self.send(target, ':%s %s %s %s' %
            (self.name, raw, target['nick'], args))

    def send(self, targets, message):
        if type(targets) is set:
            tags = ','.join(target['tag'] for target in targets)
        else:
            tags = targets['tag']

        self.redis.publish('output', '%s %s\r\n' % (tags, message))

    def disconnect(self, user):
        self.redis.publish('output', '%s ' % user['tag'])

    def load_user(self, tag):
        serialized = self.redis.get(tag)
        return serialized and json.loads(serialized)

    def save_user(self, user):
        serialized = json.dumps(user)
        self.redis.set(user['tag'], serialized)
