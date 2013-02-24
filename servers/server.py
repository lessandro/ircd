import redisutil


class Server(object):
    def __init__(self, name):
        self.name = name
        self.users = {}
        self.sub = redisutil.RedisSub('output', self.server_message)
        self.mq = redisutil.RedisMQ('input')

        self.mq.send('reset %s ' % name)
        self.buffers = {}

    def make_tag(self, address, port):
        return '%s-%s-%s' % (self.name, address, port)

    def server_message(self, message):
        targets, message = message.split(' ', 1)

        for target in targets.split(','):
            if target in self.users:
                self.users[target](message)

    def user_connect(self, tag, address, handler):
        self.users[tag] = handler
        self.buffers[tag] = []
        self.mq.send('connect %s %s' % (tag, address))

    def user_message(self, tag, data):
        buf = self.buffers[tag]
        while True:
            index = data.find('\n')
            if index == -1:
                buf.append(data)
                break
            buf.append(data[:index])
            data = data[index + 1:]
            message, buf[:] = ''.join(buf).strip(), []
            if message:
                self.mq.send('message %s %s' % (tag, message))

    def user_disconnect(self, tag, reason=''):
        del self.users[tag]
        del self.buffers[tag]
        self.mq.send('disconnect %s %s' % (tag, reason))
