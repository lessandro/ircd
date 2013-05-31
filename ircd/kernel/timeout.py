import collections
import time


class Timeout(object):
    """
    Ping timeout tracker

    The server will wait for ping_timeout seconds of inactivity to
    send a PING message, then wait for ping_timeout more seconds before
    disconnecting the user.
    """
    def __init__(self, server, config):
        self.server = server
        self.ping_timeout = config.ping_timeout

        # list of tags to check later
        # this queue will have ping_timeout seconds worth of tags
        self.check_later = collections.deque()

        # tag -> (last seen, sent ping?)
        self.last_seen = {}

    def check(self):
        """
        Check the check_later queue to see who needs to be pinged or
        disconnected
        """
        now = time.time()

        while self.check_later:
            tag, ctime = self.check_later[0]

            # only check tags whose events happened ping_timeout seconds ago
            if now - ctime < self.ping_timeout:
                break

            self.check_later.popleft()

            # user disconnected
            if tag not in self.last_seen:
                continue

            last_message, sent_ping = self.last_seen[tag]

            if now - last_message >= 2 * self.ping_timeout:
                if sent_ping:
                    self.server.disconnect({'tag': tag})
                    # remove tag from tracker to avoid disconnecting twice
                    self.remove(tag)
                    continue

            if now - last_message >= self.ping_timeout:
                if not sent_ping:
                    self.server.send(tag, 'PING :%s' % self.server.name)
                    self.check_later.append((tag, now))
                    self.last_seen[tag] = (last_message, True)

    def update(self, tag):
        """
        Update the last_seen dict and schedule this tag for later checking
        """
        now = time.time()
        self.check_later.append((tag, now))
        self.last_seen[tag] = (now, False)

    def remove(self, tag):
        """
        Stop tracking this tag

        Any occurrences of this tag in check_later will be discarded
        during check()
        """
        if tag in self.last_seen:
            del self.last_seen[tag]
