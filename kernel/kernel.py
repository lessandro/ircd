import logging
import command
import redis


class Kernel(object):
    def __init__(self, config):
        self.name = config.server_name
        self.users = {}
        self.chans = {}

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

    def user_message(self, user, message):
        logging.debug('message %s %s', user, message)

        command.dispatch(self, user, message)

    def user_connect(self, user, address):
        logging.debug('connect %s %s', user, address)

    def user_disconnect(self, user, reason):
        logging.debug('disconnect %s %s', user, reason)

    def server_reset(self, prefix):
        logging.debug('reset %s', prefix)

    def send(self, user, message):
        self.redis.publish('output', '%s %s\r\n' % (user, message))

    def disconnect(self, user):
        self.redis.publish('output', '%s ' % user)
