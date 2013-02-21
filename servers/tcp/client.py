import logging


class Client(object):
    def __init__(self, stream, address, redis):
        self.stream = stream
        self.address = address[0]
        self.redis = redis

        self.stream.read_until_close(self.on_chunk, self.on_chunk)
        self.stream.set_close_callback(self.on_disconnect)

    def on_chunk(self, data):
        # split messages
        self.redis.rpush('input', data.decode('utf-8').strip())

    def on_connect(self):
        print 'connected'

    def on_disconnect(self):
        self.stream = None

    def send(self, message):
        try:
            self.stream.write(message.encode('utf-8'))
        except:
            logging.debug('error sending msg to %s' % repr(self.address))
