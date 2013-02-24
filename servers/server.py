import redisutil


class Server(object):
    def __init__(self, name):
        self.name = name
        self.users = {}
        self.sub = redisutil.RedisSub('output', self.server_message)
        self.mq = redisutil.RedisMQ('input')

        self.mq.send('reset %s ' % name)

    def make_tag(self, address, port):
        return '%s-%s-%s' % (self.name, address, port)

    def server_message(self, message):
        targets, message = message.split(' ', 1)

        for target in targets.split(','):
            if target in self.users:
                self.users[target](message)

    def user_connect(self, tag, address, handler):
        self.users[tag] = handler
        self.mq.send('connect %s %s' % (tag, address))

    def user_message(self, tag, message):
        self.mq.send('message %s %s' % (tag, message))

    def user_disconnect(self, tag, reason=''):
        del self.users[tag]
        self.mq.send('disconnect %s %s' % (tag, reason))
