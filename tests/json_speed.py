from __future__ import with_statement
from timer import timer
import cPickle
import json
import simplejson
import cjson
import ujson
import msgpack
import marshal

cjson.dumps = cjson.encode
cjson.loads = cjson.decode

data = {
    'tag': 'tcp-127.0.0.1-12345',
    'nick': 'nick_nick_nick',
    'auth': True,
    'username': '~username',
    'ip': '127.0.0.1',
    'id': 'nick_nick_nick!~username@127.0.0.1',
    'modes': ['i', 'a', 'b', ('k', '1235')],
    'timestamp': 123456789
}

n = 10000

for lib in [cPickle, json, simplejson, cjson, ujson, msgpack, marshal]:
    print lib.__name__

    with timer:
        for i in xrange(n):
            lib.dumps(data)

    print '  dumps', n / timer.duration()

    serialized = lib.dumps(data)
    with timer:
        for i in xrange(n):
            lib.loads(serialized)

    print '  loads', n / timer.duration()

print '(actions per second)'
