import tornado
import redisutil


class Server(object):
    def __init__(self, name, config):
        self.name = name
        self.users = {}
        self.buffers = {}

        self.mq = redisutil.RedisMQ('mq:kernel', config.redis_db)
        self.mq_in = redisutil.RedisMQ('mq:' + self.name, config.redis_db)

    def stop(self):
        self.mq.send('reset %s server stop' % self.name)

    @tornado.gen.engine
    def connect(self, callback=None):
        yield tornado.gen.Task(self.mq.connect)
        yield tornado.gen.Task(self.mq_in.connect)
        self.mq_in.loop(self.server_message)
        self.mq.send('reset %s server restart' % self.name)
        callback()

    def make_tag(self, address, port):
        address = address.replace(':', '_')
        return '%s:%s-%s' % (self.name, address, port)

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
        if tag in self.users:
            del self.users[tag]
            del self.buffers[tag]
            self.mq.send('disconnect %s %s' % (tag, reason))
