import redisutil


class Server(object):
    def __init__(self, name):
        self.name = name
        self.users = {}
        self.sub = redisutil.RedisSub('output', self.server_message)
        self.mq = redisutil.RedisMQ('input')

        self.mq.send('reset %s' % name)

    def server_message(self, message):
        pass

    def user_connect(self, tag, address):
        self.users[tag] = 1
        self.mq.send('connect %s-%s %s' % (self.name, tag, address))

    def user_message(self, tag, message):
        self.mq.send('message %s-%s %s' % (self.name, tag, message))

    def user_disconnect(self, tag):
        del self.users[tag]
        self.mq.send('disconnect %s-%s' % (self.name, tag))
