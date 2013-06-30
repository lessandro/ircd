# ircd

A hot-swappable, non-compliant IRCd.

Hot-swappable in the sense that you can update the server code while it's
running without disconnecting any users.

RFC compliance is not a goal, neither in completeness nor in correctness.
This IRCd is inspired by the late MSN chat server, and most notably implements
the following features:

- Two different users can login with the same nick simultaneously. This allows
a user to access multiple channels via different browser pages (and thus
multiple connections). PRIVMSGs to a certain nick will reach all users with
that nick.

- The authentication process is very strict, and nick changes are not allowed.

- There's an additional channel/user mode, +q (channel owner), which is
stronger than channel operator.

- Channel access control via the ACCESS command (see the IRCX draft in doc/).

## Architecture

The listening endpoints (SockJS and plain TCP) are completely decoupled from
the proper IRC server, and communicate with each other through a makeshift
message queue implemented via blocking operations on redis lists.

All user and channel data is persisted in redis at all times; the server has
to fetch and update the relevant data bits while processing each and every
message from the client. That is pretty slow. Don't expect to process more than
100 messages per second with this IRCd.

                         tornado                                      irc
                        endpoints                redis               server
                      +-----------+         +-------------+       +----------+
     browsers   <---> |  sockjs   | <--+--> |  blpop mq   | <---> |  server  |
                      +-----------+    |    |             |       +----------+
                      +-----------+    |    |  chan/user  |            ^
    irc clients <---> | tcp(6667) | <--+    |    data     | <----------+
                      +-----------+         +-------------+

## Installation

Clone the repository:

    git clone https://github.com/lessandro/ircd.git
    cd ircd

Grab the dependencies:

    redis-server
    pip install -r requirements.txt

Configure:

    vim config/config.py

Start the servers:

    bin/runservers

The servers run inside supervisord.

See www/index.html for an example of a SockJS client.

## Hotswapping

As long as the endpoints remain intact, you can hotswap the server by simply
running `bin/ctl restart kernel`. This command tells supervisord to send a
SIGTERM and then restart the server. No messages are dropped and the sighandler
will let the server finish processing any current message before exiting the
process.

    # git pull or edit files
    bin/ctl restart kernel

The `bin/watch` script detects changes in the source files and automaticaly
restarts the server if the unit tests pass.

    pip install pywatch
    bin/watch

## Supervisord ctl

Access the supervisord ctl with `bin/ctl`. Any parameters are forwarded to
supervisorctl.

    # to access the supervisorctl cli
    bin/ctl

    # just print the status and exit
    bin/ctl status

    # stop everything
    bin/ctl stop all
    bin/ctl shutdown

    # wipe the database
    bin/flushdb

## Testing

The unit tests use py.test and the code coverage plugin. You can run the tests
with the command below, but if you're actively developing you should be using
the watch script as described in the hotswapping section.

    bin/runtests

## License

Copyright (C) 2013 Lessandro Mariano

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
