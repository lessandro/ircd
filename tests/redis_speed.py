from __future__ import with_statement
from timer import timer
import redis
import time

r = redis.StrictRedis()
t = time.time
n = 10000

with timer:
    for i in xrange(n):
        r.sadd('test', str(i % 1000))
        r.srem('test', str((i + 500) % 1000))

r.delete('test')

print timer.duration() / n / 2
