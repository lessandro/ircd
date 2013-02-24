import redis


def start(config):
    r = redis.StrictRedis()
    print 'kernel initialized'

    def send(message):
        r.publish('output', message + '\r\n')

    while True:
        _, message = r.blpop('input')
        print repr(message)

        command, origin, data = message.split(' ', 2)

        if command == 'connect':
            send('%s hello %s' % (origin, data))

        if command == 'message':
            send('%s you sent %d chars: %s' % (origin, len(data), data))
            if data == 'quit':
                r.publish('output', '%s ' % origin)

        if command == 'disconnect':
            send('%s goodbye' % origin)
