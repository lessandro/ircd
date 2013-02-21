import redis

r = redis.StrictRedis()
print 'kernel initialized'

while True:
    _, message = r.blpop('input')
    print message
    r.publish('output', 'hello ' + message)
