# ircd

A hot-swappable, non-compliant IRCd.

## Architecture

                         tornado                                        irc
                        endpoints                 redis                server
                      +-----------+           +-------------+       +----------+
     browsers   <---> |  sockjs   | <---+---> |  blpop mq   | <---> |  server  |
                      +-----------+     |     |             |       +----------+
                      +-----------+     |     |  chan/user  |            ^
    irc clients <---> | tcp(6667) | <---+     |    data     | <----------+
                      +-----------+           +-------------+

## Dependencies

    redis-server
    pip install -r requirements.txt

## Configuration

    vim config/config.py

## Running

    bin/runservers

## Testing

    bin/runtests

## Supervisord ctl

    bin/ctl

## Update kernel

    git pull # or edit files
    bin/ctl restart kernel

Automatically:

    pip install pywatch
    bin/watch

## Stopping

    bin/ctl stop all
    bin/ctl shutdown

## License

GPLv3
