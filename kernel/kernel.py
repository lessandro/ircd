import redis


def start(config):
    r = redis.StrictRedis()
    print 'kernel initialized'

    while True:
        _, message = r.blpop('input')
        print message
        r.publish('output', 'msg ' + message)
